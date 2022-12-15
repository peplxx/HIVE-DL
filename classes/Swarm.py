from Leader import Leader
from Drone import Drone
from math import floor


class Swarm:
    """Если is_new, то создаём нового лидера и новую группу дронов,
    иначе берём из *args первого как лидера, остальных - как ведомых (уже существуют)"""
    def __init__(self, is_new, num_of_group, num_of_drones, sim_object, *args):
        self.ind = num_of_group
        self.num = num_of_drones
        self.is_free = True
        self.sim = sim_object
        if is_new:
            self.leader = Leader(f"Leader|{self.ind}", sim_object)
            self.drones = []
            for i in range(self.num - 1):
                self.drones.append(Drone(f"Drone|{self.ind}|{i}", sim_object))
        else:
            self.leader = args[0]  # перевести в лидера
            self.drones = args[1:]

    def merge(self, another_swarm):
        self.drones += another_swarm.drones
        self.num_of_drones += 1 + len(another_swarm.drones)
        # упразднить лидера

    def separate(self, factor, new_number):
        new_drones = self.drones[:floor(self.num * factor)]
        new_group = Swarm(False, new_number, floor(self.num * factor), self.sim, new_drones)
        self.num_of_drones -= floor(self.num * factor)
        self.drones = self.drones[floor(self.num * factor):]
        return new_group

    def do_task(self):
        """Создать файл со всеми типами заданий"""
        pass
