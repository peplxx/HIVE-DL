class Vector3(object):
    def __init__(self, arr):
        if type(arr) == Vector3:
            self.vector = arr.vector
        else:
            self.vector = arr[:3]

    def __add__(self, other):
        return Vector3([self.vector[i] + other.vector[i] for i in [0, 1, 2]])

    def __sub__(self, other):
        return Vector3([self.vector[i] - other.vector[i] for i in [0, 1, 2]])

    def __mul__(self, a: int):
        return Vector3([self.vector[i] - a for i in [0, 1, 2]])

    @property
    def length(self):
        return abs((sum([self.vector[i] ** 2 for i in [0, 1, 2]])) ** .5)

    def divisizon(self,a):
        return Vector3([self.vector[i] / a for i in [0, 1, 2]])