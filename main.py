import zmqRemoteApi
from zmqRemoteApi import RemoteAPIClient
client = RemoteAPIClient()

sim = client.getObject('sim')
h = sim.getObjects('/target')
print(h)
