class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dist(self, point):
        return self.square_of_dist(point) ** 0.5

    def square_of_dist(self, point):
        return (point.x - self.x) ** 2 + (point.y - self.y) ** 2 + (point.z - self.z) ** 2
