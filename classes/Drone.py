

class Drone:
    def __init__(self, name, sim_object):
        self.max_velocity = 0.3
        self.max_acceleration = 0.025
        self.max_jerking = 80
        self.sim = sim_object
        self.name = name

        self.object = self.sim.loadModel('hackaton_models/copter.ttm')

        # self.object = self.sim.getObject(f'/{self.name}')
        self.target_object = None
        self.set_target()
        print(f'Drone #{self.object} initialized!')

    def cb(self,pose, vel, accel, handle):
        self.sim.setObjectPose(handle, -1, pose)

    def get_drone_position(self):
        return self.sim.getObjectPose(self.object, -1)

    def get_position(self, object):
        return self.sim.getObjectPose(object, -1)

    def set_target(self):
        self.target_object = self.sim.getObject(f"/{self.name}/target")
        self.sim.setObjectParent(self.target_object, -1, True)
        print(self.target_object)

    def move_target(self, target_pose):
        start_pose_target = self.get_position(self.target_object)
        self.sim.moveToPose(-1, start_pose_target, [self.max_velocity], [self.max_acceleration], [self.max_jerking],
                            target_pose,
                            self.cb,
                            self.target_object,
                            [1, 1, 1, 0.1])
        # self.sim.setObjectPose(self.target_object, -1, target_pose)
