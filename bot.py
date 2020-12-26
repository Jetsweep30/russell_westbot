import yaml
from twitchio.ext import commands
from playsound import playsound

import os.path

import requests
import random
import pandas as pd

import sound_effect

import time
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


def memoize_greeting(f):
    memo = {'russell_westbot': 1}
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
    print(ctx)
    #make sure the bot ignores itself and the streamer
    #if ctx.author.name.lower() == 'jetsweep30':
       # return

    #await ctx.channel.send(ctx.content)
    await bot.handle_commands(ctx)

    '''if 'hello' in ctx.content.lower():'''
    try:
        await greeting(ctx)
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

    if os.path.isfile('./soundboard/{}.mp3'.format(sound_name)):
        await ctx.send('file "{}.mp3" already exists, use !addf to overwrite'.format(sound_name))
    else:
        try:
            sound_url = sound_info[2]
            sound_start = sound_info[3]
            sound_volume = .06
            try:
                sound_length = min(int(sound_info[4]), 7)
            except:
                sound_length = 7
            sound_effect.do_all(name=sound_name, url=sound_url, start=sound_start, length=sound_length, volume=sound_volume)
            await ctx.send('nice! thanks for adding "!sound {}"'.format(sound_name))
            playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(sound_name))
        except:
            await ctx.send('didn\'t work try this format...')
            time.sleep(1.2)
            await ctx.send('!add [name] [url] [start_time] [length]')
            time.sleep(1.3)
            await ctx.send('for example... !add jets 7sllUioMHJY 1:03 7')

@bot.command(name='addf')
async def addf(ctx):

    try:
        sound_info = ctx.content.split(" ")
        sound_name = sound_info[1].lower()
        sound_url = sound_info[2]
        sound_start = sound_info[3]
        sound_volume = .06
        try:
            sound_length = min(int(sound_info[4]), 7)
        except:
            sound_length = 7
        sound_effect.do_all(name=sound_name, url=sound_url, start=sound_start, length=sound_length, volume=sound_volume)
        await ctx.send('nice! thanks for adding "!sound {}"'.format(sound_name))
        playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(sound_name))
    except:
        await ctx.send('didn\'t work try this format...')
        time.sleep(1.2)
        await ctx.send('!addf [name] [url] [start_time] [length]')
        time.sleep(1.3)
        await ctx.send('for example... !addf jets 7sllUioMHJY 1:03 7')

@bot.command(name='addv')
async def addv(ctx):
    try:
        sound_info = ctx.content.split(" ")
        sound_name = sound_info[1].lower()
        sound_url = sound_info[2]
        sound_start = sound_info[3]
        if float(sound_info[5]) > 1:
            sound_volume = float(sound_info[5])/100
        else:
            sound_volume = float(sound_info[5])
        try:
            sound_length = int(sound_info[4])
        except:
            sound_length = 7
        sound_effect.do_all(name=sound_name, url=sound_url, start=sound_start, length=sound_length, volume=sound_volume)
        await ctx.send('nice! thanks for adding "!sound {}"'.format(sound_name))
        playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(sound_name))
    except:
        await ctx.send('didn\'t work try this format...')
        time.sleep(1.2)
        await ctx.send('!addf [name] [url] [start_time] [length]')
        time.sleep(1.3)
        await ctx.send('for example... !addf jets 7sllUioMHJY 1:03 7')


@bot.command(name='sound')
async def sound(ctx):
    sound_info = ctx.content.split(" ")
    sound_name = sound_info[1].lower()
    try:
        playsound('/Users/jletienne/russell_westbot/soundboard/{}.mp3'.format(sound_name))
    except:
        time.sleep(.7) #it makes it seem like I looked lol
        await ctx.channel.send('i couldn\'t find that sound')

@bot.command(name='zenefits')
async def zenefits(ctx):
    await playsound('/Users/jletienne/Music/Logic/soundboard/jetsweep30_zenefits.wav')


@bot.command(name='go')
async def go(ctx):
    await playsound('/Users/jletienne/Music/Logic/soundboard/dababy_bop.wav')

@bot.command(name='go2')
async def go2(ctx):
    await playsound('/Users/jletienne/Music/Logic/soundboard/dababy_letsgo_3.wav')

@bot.command(name='go3')
async def go3(ctx):
    await playsound('/Users/jletienne/Music/Logic/soundboard/dababy_letsgo_2.wav')

@bot.command(name='hot')
async def hot(ctx):
    await playsound('/Users/jletienne/Music/Logic/soundboard/dababy_hot.wav')

@bot.command(name='huh')
async def huh(ctx):
    await playsound('/Users/jletienne/Music/Logic/soundboard/dababy_huh.wav')

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
