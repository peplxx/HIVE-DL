from classes.Task import Task
from classes.Point import Point
from classes.Swarm import Swarm
from params.values import lidar_radius

"""
      -→|‾‾‾‾‾‾‾‾‾‾‾‾|
 left | │            │
 side | │            │
      -→|____________|
        ↑           ↑
        |-----------|
         bottom side
"""


class CoveringOfAreaTask(Task):
    def __init__(self, swarm: Swarm, height: int, LDx: int, LDy: int, RTx: int, RTy: int):
        super(CoveringOfAreaTask).__init__(swarm)  # Init task with group of drones
        self.LDPoint = Point(LDx, LDy, height)  # Left-Down point of rectangle
        self.RTPoint = Point(RTx, RTy, height)  # Right-Top point of rectangle
        self.LTPoint = Point(LDx, RTy, height)  # Left-Top point of rectangle
        self.RDPoint = Point(RTx, LDy, height)  # Right-Down point of rectangle
        self.left_side = self.LTPoint.dist(self.LDPoint)  # The left side of rectangle (watch up)
        self.bottom_side = self.LDPoint.dist(self.RDPoint)  # The bottom side of rectangle (watch up)
        if self.left_side / self.group.get_size > lidar_radius:
            if self.bottom_side < self.left_side:
                self.bottom_side, self.left_side = self.left_side, self.bottom_side
                self.LDPoint, self.LTPoint, self.RDPoint, self.RTPoint = self.LTPoint, self.RTPoint, self.LDPoint, self.RDPoint
