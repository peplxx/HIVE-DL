import asyncio

from classes.Drone import Drone
from classes.Vector import Vector3


async def calc_dist_to_drone(pos1, pos2):
    return ((pos1 - pos2).length, pos2)


async def p_get_drones_positions(drones, leader):
    dronlist = drones + [leader]
    return await asyncio.gather(*([
        drone.get_self_position() for drone in dronlist
    ]
    ))


async def get_drones_positions(drones, leader, index, radius):
    dronlist = drones
    all_drones = await asyncio.gather(*[
        drone.get_self_position() for drone in dronlist
    ]
                                      )
    result = [await leader.get_self_position()]
    sort_by_distance = [
        await calc_dist_to_drone(all_drones[index], dronpos)
        for cur, dronpos in enumerate(all_drones[:-1]) if cur != index
    ]
    sort_by_distance.sort()
    print("sfdgfh", len(sort_by_distance[:2]))
    result += [elem[1] for elem in sort_by_distance[:2]]
    return result


class Follower(Drone):
    def __init__(self, name, sim_object, distance=1):
        super().__init__(name, sim_object)
        self.dist = distance

    async def calc_next_pos(self, drone_positions, const, drone_index):
        sumarize = Vector3([0, 0, 0])
        k1, k2 = 0.1, 0.1
        for index, dronpos in enumerate(drone_positions):
            if index != drone_index:
                v = dronpos
                to_drone = (v - self.position)
                from_drone = (self.position - v)
                l = to_drone.length
                if l > self.dist:
                    result = to_drone * (l - self.dist) * k1
                else:
                    result = from_drone * (self.dist - l) * k2
                sumarize += result
        self.speed += sumarize
        self.speed = self.speed.divisizon(const)
        new_position = (self.position + self.speed).vector
        new_position[2] = self.position.vector[2]
        return Vector3(new_position)

    async def start_moving(self, drones, leader, drone_index):
        CONSTANT = 50
        while self.isAlive:
            drone_positions = await get_drones_positions(drones, leader , drone_index, 1.5)
            next_pos = await self.calc_next_pos(drone_positions, CONSTANT, drone_index)
            print(drone_index)
            target_pose = next_pos.vector
            start_pose_target = await self.sim.getObjectPose(self.target_object, -1)
            position = [target_pose[0], target_pose[1], target_pose[2]] \
                       + start_pose_target[3:]
            await self.sim.setObjectPose(self.target_object, -1, position)
            await asyncio.sleep(0)
