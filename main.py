import asyncio
import sys
import zmqRemoteApi
from classes.Follower import Follower
from zmqRemoteApi.asyncio import RemoteAPIClient
from classes.Drone import Drone


def invert(xyz, a):
    return [xyz[0] + a, xyz[1], xyz[2]] + xyz[3:]


async def get_drones_positions(drones, leader):
    return await asyncio.gather(*([
                                      drone.get_self_position() for drone in drones
                                  ] + [leader.get_self_position()]
                                  ))


async def update_positions(drones, leader):
    drone_positions = await get_drones_positions(drones, leader)
    next_drone_positions = await asyncio.gather(*[
        drone.calc_next_pos(drone_positions, 1) for drone in drones
    ])
    print(*[n.vector for n in next_drone_positions])
    await asyncio.gather(*[
        drone.move_target(next_pos) for drone, next_pos in zip(drones, next_drone_positions)
    ])
    await asyncio.sleep(0)


async def start_drones(drones, leader):
    await asyncio.gather(
        *[drone.start_moving(drones, leader, index) for index,drone in enumerate(drones)]
    )


"""
path = [(1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0), (1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0),
                (1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0), (1, 10, 2, 0, 0, 0), (1, 1, 1, 0, 0, 0),
                (1, 10, 2, 0, 0, 0)] (путь дронов - сеятелей бахчи пусть это останется в памяти проекта 2022)
"""


async def main():
    async with RemoteAPIClient() as client:
        sim = await client.getObject('sim')

        defaultIdlsFps = await sim.getInt32Param(sim.intparam_idle_fps)
        await sim.setInt32Param(sim.intparam_idle_fps, 0)

        print("Success hooked client ...")
        num_of_drones = 2
        leader = Drone(f"leader", sim)
        drones = [Follower(f"copter{i}", sim) for i in range(1, num_of_drones + 1)]
        await asyncio.gather(*([
                                   drone.set_target_and_object() for drone in drones
                               ] + [leader.set_target_and_object()]))
        print("Initialized all drones...")

        await start_drones(drones, leader)

    print("Program ended")


if sys.platform == 'win32' and sys.version_info >= (3, 8, 0):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
