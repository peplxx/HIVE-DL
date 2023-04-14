import asyncio

from classes.Drone import Drone
from classes.Vector import Vector3


class Follower(Drone):
    def __init__(self, name, sim_object, controller, distance=1):
        super().__init__(name, sim_object, controller)
        self.dist = distance

    async def calc_next_pos(self, nearest_drones,leader_position):
        speed_vector = await self.controller.speed_calc(nearest_drones,leader_position, self.position)
        self.speed += speed_vector
        self.speed = self.speed.divisizon(self.controller.speed_const)

        new_position = (self.position + self.speed).vector
        new_position[2] = self.position.vector[2]  # сохраняем высоту
        return Vector3(new_position)

    async def start_moving(self, drone_index):
        while self.isAlive:
            nearest_drones = await asyncio.gather(
                self.controller.get_nearest_drones(2, drone_index, leader_affect=True)

            )
            print(nearest_drones)
            target_position = await asyncio.gather(
                self.calc_next_pos(nearest_drones)
            )
            target_position = target_position.vector


            rotation_info = await self.sim.getObjectPose(self.target_object, -1)[3:]
            position = [*target_position] \
                       + rotation_info
            await self.sim.setObjectPose(self.target_object, -1, position)
            await asyncio.sleep(0)

    async def move(self, target_position):
        rotation_info = await self.sim.getObjectPose(self.target_object, -1)
        rotation_info = [0,0,0]
        position = [*target_position] \
                   + rotation_info
        print("11111111111111")
        await self.sim.setObjectPose(self.target_object, -1, position)