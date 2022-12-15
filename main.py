import zmqRemoteApi
from zmqRemoteApi import RemoteAPIClient
from classes.Drone import Drone

client = RemoteAPIClient()
sim = client.getObject('sim')
print("Success hooked client ...")

new_drone = Drone('copter', sim)
print(new_drone.get_drone_position())
print("Initialized all drones...")

while new_commad := input('enter command: '):
    args = list(map(int, new_commad.split()))
    new_pos = args + [0, 0, 0, -1]
    new_drone.move_target(new_pos)

print("Program ended")
