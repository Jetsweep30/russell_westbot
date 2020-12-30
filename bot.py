import yaml
from twitchio.ext import commands
from playsound import playsound

import os.path

import requests
import random
import pandas as pd

import sound_effect

import time

import random
# create the bot account
# pass parameters into the bot
# set up movies

# memoize hello

#dak_prescbot is next
#leBot_james is after
#jj_bot is after that

token = yaml.safe_load(open('config.yaml'))['token']
client_id = yaml.safe_load(open('config.yaml'))['client_id']
client_secret = yaml.safe_load(open('config.yaml'))['client_secret']


bot = commands.Bot(
    # set up the bot
    irc_token=token,
    client_id=client_id,
    nick='russell_westbot',
    prefix='!',
    initial_channels=['jetsweep30']
)


mods = {'russell_westbot': 1, 'jetsweep30': 1, 'streamlabs': 1}

def memoize_greeting(f):
    memo = {'russell_westbot': 1, 'jetsweep30': 1, 'streamlabs': 1}
    def helper(x):
        if x.author.name not in memo:
            memo[x.author.name] = 1
            return f(x)
        return None
    return helper


@memoize_greeting
def greeting(ctx):
    greeting = 'hello {}'.format(ctx.author.name)
    try:
        playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(ctx.author.name.lower()))
        return ctx.channel.send(greeting)
    except:
        playsound('/Users/jletienne/russell_westbot/soundboard/quicksand.mp3')
        return ctx.channel.send('welcome to the stream {}! you should !add a custom theme song'.format(ctx.author.name))



@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg('jetsweep30', f"/me has landed!")


@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    #print(ctx)
    #make sure the bot ignores itself and the streamer
    #if ctx.author.name.lower() == 'jetsweep30':
       # return


    print(f'{ctx.author.name}: {ctx.content}\n')
    try:
        await bot.handle_commands(ctx)
    except:
        pass

    '''if 'hello' in ctx.content.lower():'''
    try:
        await greeting(ctx)
    except:
        pass

    #playsound if it exists
    if ctx.content[0] == '!':
        try:
            await playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(ctx.content[1:].lower()))
        except:
            pass

@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='bandcamp')
async def bandcamp(ctx):
    await ctx.send('jetsweep30.bandcamp.com')

@bot.command(name='github')
async def github(ctx):
    await ctx.send('https://github.com/jetsweep30/russell_westbot')

@bot.command(name='add')
async def add(ctx):

    sound_info = ctx.content.split(" ")
    sound_name = sound_info[1].lower()

    #should people be able to overwrite sounds?
    '''if os.path.isfile('./soundboard/{}.mp3'.format(sound_name)): #1 == 0
        await ctx.send('file "{}.mp3" already exists, use !addf to overwrite'.format(sound_name))
    else:'''
    try:
        sound_url = sound_info[2]
        sound_start = sound_info[3]
        sound_volume = .12
        try:
            sound_length = min(int(sound_info[4]), 7)
        except:
            sound_length = 7
        sound_effect.do_all(name=sound_name, url=sound_url, start=sound_start, length=sound_length, volume=sound_volume)
        await ctx.send('nice! thanks {} for adding "!sound {}"'.format(ctx.author.name, sound_name))
        playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(sound_name))
    except:
        await ctx.send('didn\'t work try this format...')
        time.sleep(1.2)
        await ctx.send('!addf [name] [url] [start_time] [length]')
        time.sleep(1.3)
        await ctx.send('for example... !addf jets 7sllUioMHJY 1:03 7')



# play a random gyfe from the triggerfyre obs intergration
@bot.command(name='gif')
async def gif(ctx):
    gifs = ['bullet', 'fail',  'perfect', 'steph', 'check', 'jwill', 'marshawn', 'salsa', 'vince', 'davante', 'lavine', 'obj', 'shake', 'dougie', 'lebron', 'over', 'shimmy']
    await ctx.channel.send('!' + random.choice(gifs))

# play a random sound from the /soundboard
@bot.command(name='sound')
async def sound(ctx):
    sounds = [sound[:-4] for sound in os.listdir('./soundboard') if sound[-4:] == '.mp3']
    await ctx.channel.send('!' + random.choice(sounds))

# fix the message so multiple things can happen
'''async def play_the_sound(path):'''

# alerts
@bot.command(name='alert')
async def alert(ctx):
    alert_info = ctx.content.split(" ")
    alert_type = alert_info[1].lower()[:-1]

    if ctx.author.name in mods:
        try:
            sounds = [sound[:-4] for sound in os.listdir('./soundboard/alerts/{}'.format(alert_type)) if sound[-4:] == '.mp3']

            await playsound('./soundboard/alerts/{}/{}.mp3'.format(alert_type, random.choice(sounds)))
        except:
            pass
    else:
        pass

# play a random sound from the /soundboard
@bot.command(name='sound_list')
async def sound_list(ctx):
    sounds = [sound[:-4] for sound in os.listdir('./soundboard') if sound[-4:] == '.mp3']
    sounds.sort()
    await ctx.channel.send(', '.join(sounds))

@bot.command(name='gif_list')
async def gif_list(ctx):
    gifs = [gif[:-4] for gif in os.listdir('./gifs') if gif[-4:] == '.gif']
    gifs.sort()
    await ctx.channel.send(', '.join(gifs))


def request_movie(ctx):
    r = requests.get('https://raw.githubusercontent.com/mastercbf/waldy/master/dicksflicks.json')
    random_num = random.randrange(0,len(r.json()))

    random_film = r.json()[random_num]

    recommendation =  'You should watch {} ({}), I gave it a {}/4!'.format(random_film['Film'], random_film['Year'], random_film['Rating'])

    return ctx.channel.send(recommendation)

def search_movie(ctx, film):
    print(film)
    r = requests.get('https://raw.githubusercontent.com/mastercbf/waldy/master/dicksflicks.json')
    x = pd.DataFrame(r.json())

    request = x[(x['Film'].str.lower() == film.lower())].reset_index()

    requested_film = request.loc[0].to_dict()

    recommendation =  'You should watch {} ({}), I gave it a {}/4!'.format(requested_film['Film'], requested_film['Year'], requested_film['Rating'])
    return ctx.channel.send(recommendation)

# recommend a movie based on richie's suggestions
@bot.command(name='movies')
async def movies(ctx):

    if len(ctx.content) < 9:
        await request_movie(ctx)
    else:
        film = ctx.content[8:]
        try:
            await search_movie(ctx, film)
        except:
            await ctx.channel.send('I can\'t find that one right now!')


if __name__ == "__main__":
    bot.run()
