import asyncio
from classes.Vector import Vector3


class SimController:
    def __init__(self):
        self.drones = []  # Список дронов
        self.leader = None  # Дрон - лидер
        self.speed_const = 50  # Магическая константа для скорости
        self.total_drones = None  # Общее количество дронов
        self.k1, self.k2 = 0.5, 0.5  # Еще магические константы
        self.req_distance = 1  # Константа регулировки дистанции между дронами
        self.sim = None
    async def init(self, drones, leader, sim_object):
        self.drones = drones
        self.leader = leader
        self.total_drones = len(drones)
        self.sim = sim_object

    async def start_drones(self):
        # Запускает метод баражирования у дронов
        await asyncio.gather(
            *[drone.start_moving(index)
              for index, drone in enumerate(self.drones)]
        )

    async def get_drones_positions(self):
        #await self.leader.get_self_position()
        # Метод для получения позиций всех дронов
        return await asyncio.gather(*[drone.get_self_position()
                                      for drone in self.drones])

    async def get_leader_position(self):
        return await asyncio.gather(self.leader.get_self_position())

    async def distance_between(self, position1: Vector3, position2: Vector3) -> int:
        # Вычисляет дистанцию между двумя точками в пространстве
        vector = (position1 - position2)
        return vector.length

    async def speed_calc(
            self, nearest_drones,
            leader_position,
            current_drone_position: Vector3):
        # Функция для расчета скорости дрона для баражирования
        result_vector = Vector3([0, 0, 0])
        for index, drone_position in enumerate(nearest_drones):
            vector_to_drone = (drone_position - current_drone_position)
            vector_from_drone = (current_drone_position - drone_position)
            if vector_to_drone.length > self.req_distance:
                result_vector += vector_to_drone * \
                                 (vector_to_drone.length - self.req_distance) * self.k1
            else:
                result_vector += vector_from_drone * \
                                 (self.req_distance - vector_from_drone.length) * self.k2
        vector_to_drone = (leader_position - current_drone_position)
        vector_from_drone = (current_drone_position - leader_position)
        if (L:=vector_to_drone.length) > self.req_distance:
            result_vector += vector_to_drone * \
                             (vector_to_drone.length - self.req_distance) * -1.5
        else:
            result_vector += vector_from_drone * \
                             (self.req_distance - vector_from_drone.length)*0.1
        return result_vector

    async def get_nearest_drones(self, n: int, drone_index: int, leader_affect: bool):
        # Возвращает позиции первых n по дистанции для выбранного дрона

        drone_positions = await self.get_drones_positions()
        distance_to_drones = await asyncio.gather(
            *[self.distance_between(position1=drone_positions[drone_index],
                                    position2=drone_position)
              for drone_position in drone_positions]
        )
        multi = [(distance_to_drones[i], drone_positions[i]) for i in range(self.total_drones)]
        multi.sort()

        result = [multi[i][1] for i in range(1, n + 1)]

        #if leader_affect:
        #    result += [self.leader.position]
        #print(drone_index, "DEBUG3")
        return result

    async def mm(self):
        i = 0
        while True:
            nearest = await asyncio.gather(
                *[
                    self.get_nearest_drones(1,drone_index,True)
                    for drone_index in range(self.total_drones)]
            )
            leader_position = await asyncio.gather(
                    self.get_leader_position())
            target_poses = await asyncio.gather(
                *[
                    drone.calc_next_pos(nearest[drone_index],leader_position[0][0])
                    for drone_index, drone in enumerate(self.drones)]
            )
            p = await asyncio.gather(
                *[
                    self.sim.setObjectPose(drone.target_object, -1, target_poses[drone_index].vector + [0,0,0,1.0])
                    for drone_index, drone in enumerate(self.drones)
            ])