from Drone import Drone


class Leader(Drone):
    def __init__(self, name, sim_object):
        super(Leader).__init__(name, sim_object)

    def move_target(self, target_pose):
        start_pose_target = self.get_position(self.target_object)
        self.sim.moveToPose(-1, start_pose_target, [self.max_velocity], [self.max_acceleration], [self.max_jerking],
                            target_pose,
                            self.cb,
                            self.target_object,
                            [1, 1, 1, 0.1])
