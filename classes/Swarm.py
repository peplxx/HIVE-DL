from Leader import Leader
from Drone import Drone
from math import floor


class Swarm:
    """Если is_new, то создаём нового лидера и новую группу дронов,
    иначе берём из *args первого как лидера, остальных - как ведомых (уже существуют)"""
    def __init__(self, is_new, num_of_group, num_of_drones, sim_object, *args):
        self.ind = num_of_group
        self.size = num_of_drones
        self.is_free = True
        self.sim = sim_object
        if is_new:
            self.leader = Leader(f"Leader|{self.ind}", sim_object)
            self.drones = []
            for i in range(self.size - 1):
                self.drones.append(Drone(f"Drone|{self.ind}|{i}", sim_object))
        else:
            self.leader = args[0]  # перевести в лидера
            self.drones = args[1:]

    def merge(self, another_swarm):
        self.drones += another_swarm.drones
        self.size += 1 + len(another_swarm.drones)
        # упразднить лидера
    @property
    def get_size(self):
        return self.size
    def separate(self, factor, new_number):
        new_drones = self.drones[:floor(self.size * factor)]
        new_group = Swarm(False, new_number, floor(self.size * factor), self.sim, new_drones)
        self.size -= floor(self.size * factor)
        self.drones = self.drones[floor(self.size * factor):]
        return new_group

    def do_task(self):
        """Создать файл со всеми типами заданий"""
        pass
