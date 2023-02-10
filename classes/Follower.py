from classes.Drone import Drone
from classes.Vector import Vector3


class Follower(Drone):
    def __init__(self, name, sim_object, distance=1):
        super().__init__(name, sim_object)
        self.dist = distance

    async def calc_next_pos(self, drone_positions):
        sumarize = Vector3([0, 0, 0])
        for dronpos in drone_positions:
            if self.position != dronpos:
                v = dronpos
                vector = (self.position - v)
                sumarize += vector.divisizon(self.dist - vector.length)
        return self.position + sumarize
