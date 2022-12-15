import zmqRemoteApi
from zmqRemoteApi import RemoteAPIClient
client = RemoteAPIClient()

sim = client.getObject('sim')
h = sim.getObject('/Floor')
print(h)
sim.stopSimulation()
