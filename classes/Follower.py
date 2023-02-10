import asyncio
from classes.Drone import Drone


class Follower(Drone):
    def __init__(self, name, sim_object, distance=1):
        super().__init__(name, sim_object)
        self.dist = distance

