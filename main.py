import zmqRemoteApi
from zmqRemoteApi import RemoteAPIClient
from classes.Drone import Drone

client = RemoteAPIClient()
sim = client.getObject('sim')
print("Success hooked client ...")

new_drone = Drone('copter', sim)
print(new_drone.get_drone_position())
print("Initialized all drones...")
path = [(1, 1, 1, 0, 0, 0), (2, 2, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0), (.5, .5, .5, 5, 5, 0)]
for xyz in path:
    new_pos = list(xyz) + [0, 0, 0, 0.5]
    new_drone.move_target(new_pos)

print("Program ended")
