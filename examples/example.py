"""Example code for communicating with a Zeptrion devices."""

""" Usage: python3 -m examples.example """

import asyncio
from pyzeptrion.blind import ZeptrionBlind
from pyzeptrion.bulb import ZeptrionBulb
from pyzeptrion.discover import ZeptrionRegistry
import logging



async def main():   
        
    """ Create a bulb, turn it on, wait 15 seconds, turn it off """
    myBulb = await ZeptrionBulb.create("192.168.0.181", 1)
    await myBulb.set_on()
    print(myBulb)
    await asyncio.sleep(5)
    await myBulb.set_off() 
    print(myBulb)  
    await myBulb.close()
    
    """ Create a Blind, close it, wait 15 seconds, open it """
      
    myBlind = await ZeptrionBlind.create("192.168.0.185",1)
    print(myBlind) 
    await myBlind.move_close()
    print(myBlind)
    await asyncio.sleep(15) 
    await myBlind.move_open()
    print(myBlind)
    await asyncio.sleep(20) 
    await myBlind.close()
       

    """ discover all Zeptrion devices in the network, close all blinds, open all blinds """
    myRegistry = await ZeptrionRegistry.create_registry()
    devices = await myRegistry.get_devices(myRegistry)
    blinds = []
    for device in devices:
        if device._type == "Blind":
            myBlind = await ZeptrionBlind.create(device.host, device.chn)
            blinds.append(myBlind)
            await myBlind.move_close()

    await asyncio.sleep(30) 

    for blind in blinds:
        await blind.move_open()
        await blind.close()
       

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


