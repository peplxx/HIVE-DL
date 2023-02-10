import asyncio
from multiprocessing import freeze_support
import sys
import zmqRemoteApi
from zmqRemoteApi.asyncio import RemoteAPIClient
from classes.Drone import Drone
import multiprocessing as mp


def invert(xyz, a):
    return [xyz[0] + a, xyz[1], xyz[2]] + xyz[3:]


async def get_drones_positions(drones):
    return await asyncio.gather(*[
        drone.get_self_position() for drone in drones
    ])


async def main():
    async with RemoteAPIClient() as client:
        sim = await client.getObject('sim')

        defaultIdlsFps = await sim.getInt32Param(sim.intparam_idle_fps)
        await sim.setInt32Param(sim.intparam_idle_fps, 0)

        print("Success hooked client ...")
        num_of_drones = 6
        drones = [Drone(f"copter{i}", sim) for i in range(1, num_of_drones + 1)]
        await asyncio.gather(*[
            drone.set_target_and_object() for drone in drones
        ])
        print("Initialized all drones...")



        print(await get_drones_positions(drones))










        path = [(1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0), (1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0),
                (1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0),
                (1, 10, 2, 0, 0, 0)]
        for xyz in path:
            new_pos = list(xyz)
            new_pos.append(-1)
            await asyncio.gather(*[
                drone.move_target(invert(new_pos, i))
                for i, drone in enumerate(drones, 1)
            ])
    print("Program ended")


if sys.platform == 'win32' and sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
