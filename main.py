import zmqRemoteApi
from zmqRemoteApi import RemoteAPIClient
from classes.Drone import Drone

client = RemoteAPIClient()
sim = client.getObject('sim')
print("Success hooked client ...")

new_drone = Drone('copter', sim)
print(new_drone.get_drone_position())

print("Program ended")
