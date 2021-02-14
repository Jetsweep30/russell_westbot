import asyncio
import simpleobsws
from playsound import playsound

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='MYSecurePassword', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def flip_request():
    try:
        await ws.connect() # Make the connection to OBS-Websocket
    except:
        pass

    data = {'scene-name': 'Webcam Scene', 'item': 'Logitech C920', 'visible': False}
    result =  await ws.call('SetSceneItemProperties', data)


    data2 = {'scene-name': 'Webcam Scene', 'item': 'Upside Down Webcam', 'visible': True}
    result2 =  await ws.call('SetSceneItemProperties', data2)

    playsound('./soundboard/alerts/effect/flip.mp3')


    await asyncio.sleep(18)


    data = {'scene-name': 'Webcam Scene', 'item': 'Upside Down Webcam', 'visible': False}
    result =  await ws.call('SetSceneItemProperties', data)


    data2 = {'scene-name': 'Webcam Scene', 'item': 'Logitech C920', 'visible': True}
    result2 =  await ws.call('SetSceneItemProperties', data2)

    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

async def show_autotune():
    await loop.run_until_complete(flip_request())
