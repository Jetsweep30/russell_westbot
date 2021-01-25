import asyncio
import simpleobsws
from playsound import playsound

loop = asyncio.get_event_loop()
ws = simpleobsws.obsws(host='127.0.0.1', port=4444, password='MYSecurePassword', loop=loop) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request(gif_pic):
    try:
        await ws.connect() # Make the connection to OBS-Websocket
    except:
        pass
    sourceSettings = {'file': '/Users/jletienne/russell_westbot/gifs/{}.gif'.format(gif_pic), 'unload': True}
    data = {'sourceName':'Gif', 'sourceSettings': sourceSettings}
    result = await ws.call('SetSourceSettings', data)



    data = {'scene-name': 'Audio and Effects Scene', 'source': 'Gif', 'render': True}
    result = await ws.call('SetSceneItemRender', data)


    try:
        #don't play music during live sports mode
        current_scene = await ws.call('GetCurrentScene')
        if current_scene !=  'Live Sports Scene':
            playsound('./soundboard/{}.mp3'.format(gif_pic))
        else:
            await asyncio.sleep(7)
    except:
        #pause seven seconds to display the gif
        await asyncio.sleep(7)

    data = {'scene-name': 'Audio and Effects Scene', 'source': 'Gif', 'render': False}
    result = await ws.call('SetSceneItemRender', data)

    await ws.disconnect() # Clean things up by disconnecting. Only really required in a few specific situations, but good practice if you are done making requests or listening to events.

async def show_gif(gif_pic):
    await loop.run_until_complete(make_request(gif_pic))
