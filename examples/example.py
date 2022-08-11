"""Example code for communicating with a Zeptrion devices."""

import asyncio
import logging
from pyzeptrion.blind import ZeptrionBlind
from pyzeptrion.bulb import ZeptrionBulb
from pyzeptrion.discover import ZeptrionRegistry


async def main():

    """Create a bulb, turn it on, wait 15 seconds, turn it off"""
    my_bulb = await ZeptrionBulb.create(ZeptrionBulb, "192.168.0.181", 1)
    await my_bulb.set_on()
    print(my_bulb)
    await asyncio.sleep(5)
    await my_bulb.set_off()
    print(my_bulb)
    await my_bulb.close()

    # Create a Blind, close it, wait 15 seconds, open it

    my_blind = await ZeptrionBlind.create(ZeptrionBlind, "192.168.0.185", 1)
    print(my_blind)
    await my_blind.move_close()
    print(my_blind)
    await asyncio.sleep(15)
    await my_blind.move_open()
    print(my_blind)
    await asyncio.sleep(20)
    await my_blind.close()

    # discover all Zeptrion devices in the network, close all blinds, open all blinds
    my_registry = await ZeptrionRegistry.create_registry(ZeptrionRegistry)
    devices = my_registry.devices
    blinds = []
    for device in devices:
        if device.type == "Blind":
            my_blind = await ZeptrionBlind.create(
                ZeptrionBlind, device.host, device.chn
            )
            blinds.append(my_blind)
            await my_blind.move_close()

    await asyncio.sleep(30)

    for blind in blinds:
        await blind.move_open()
        await blind.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
