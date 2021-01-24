import asyncio
import simpleobsws
from playsound import playsound

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='MYSecurePassword', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def autotune_request():
    try:
        await ws.connect() # Make the connection to OBS-Websocket
    except:
        pass
    data = {'sourceName': 'Samson Q2U', 'filterName': 'AutoPitch', 'filterEnabled': True}
    result = await ws.call('SetSourceFilterVisibility', data)


    await asyncio.sleep(24)


    data = {'sourceName': 'Samson Q2U', 'filterName': 'AutoPitch', 'filterEnabled': False}
    result = await ws.call('SetSourceFilterVisibility', data)

    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

async def show_autotune():
    await loop.run_until_complete(autotune_request())
