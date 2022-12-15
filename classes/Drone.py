class Drone:
    def __init__(self, name, sim_object):
        self.max_velocity = 0.1
        self.max_acceleration = 0.01
        self.max_jerking = 80
        self.sim = sim_object
        self.name = name
        self.object = self.sim.getObject(f'/{self.name}')
        self.target_object = None
        self.set_target()
        self.run()

    def get_drone_position(self):
        return self.sim.getObjectPose(self.object, -1)

    def get_position(self, object):
        return self.sim.getObjectPose(object, -1)

    def set_target(self):
        self.target_object = self.sim.getObject(f"/{self.name}/target")
        self.sim.setObjectParent(self.target_object, -1, True)
        print(self.target_object)

    def run(self):
        while True:
            print(self.get_position(self.target_object))
