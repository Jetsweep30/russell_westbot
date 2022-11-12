import yaml
from twitchio.ext import commands
from playsound import playsound
from convert import get_gif_from_giphy
from show_gif import make_request
from show_bomb  import show_bomb
from show_autotune import autotune_request
from show_flip import flip_request
import csv
fieldnames = ['message_datetime', 'message_author', 'message_content']

from datetime import datetime

import os.path

import requests
import random
import pandas as pd

import re

import sound_effect
import submit_track

import time

import random

not_live_sports_mode = True #set to true normally
# create the bot account
# pass parameters into the bot


#dak_prescbot is next
#leBot_james is after
#jj_bot is after that

token = yaml.safe_load(open('config.yaml'))['token']
client_id = yaml.safe_load(open('config.yaml'))['client_id']
client_secret = yaml.safe_load(open('config.yaml'))['client_secret']

allow_new_intro = True

bot = commands.Bot(
    # set up the bot
    irc_token=token,
    client_id=client_id,
    nick='russell_westbot',
    prefix='!',
    initial_channels=['jetsweep30']
)


'''with open('media/chat_history.csv', 'a', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)'''

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
    greeting = 'welcome back {}'.format(ctx.author.name)
    try:
        playsound('./soundboard/{}.mp3'.format(ctx.author.name.lower()))
        time.sleep(45)
        return ctx.channel.send(greeting)
    except:
        if not_live_sports_mode and allow_new_intro:
            try:
                greetings = [greeting for greeting in os.listdir('./soundboard/alerts/new_chat') if gif[-4:] == '.wav']

                playsound(f'./soundboard/{random.choice(greetings)}')
            except:
                playsound('./soundboard/new_chat.mp3')
            #pass
        time.sleep(33)
        return ctx.channel.send('welcome to the stream {}!'.format(ctx.author.name))



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


    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f'{current_datetime[-8:]} {ctx.author.name}:\n{ctx.content}\n')



    with open('media/chat_history.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'message_datetime': current_datetime, 'message_author': ctx.author.name, 'message_content': ctx.content})


    try:
        await greeting(ctx)
    except:
        pass

    try:
        await bot.handle_commands(ctx)
    except:
        pass

    #play media if it exists
    if ctx.content[0] == '!':
        try:
            content = ctx.content[1:].lower()
            if  content in [gif[:-4] for gif in os.listdir('./gifs') if gif[-4:] == '.gif']:
                await make_request(gif_pic = content)
            else:
                if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
                    playsound('./soundboard/{}.mp3'.format(content))
        except:
            pass
    else:
        pass

@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='bomb', aliases=['bombs','bombs_away'])
async def bomb(ctx):
    await show_bomb()

@bot.command(name='bandcamp')
async def bandcamp(ctx):
    await ctx.send('jetsweep30.bandcamp.com')

@bot.command(name='github')
async def github(ctx):
    await ctx.send('https://github.com/jetsweep30/russell_westbot')

@bot.command(name='autotune')
async def autotune(ctx):
    playsound('./soundboard/alerts/effect/autotune.mp3')
    await autotune_request('AutoPitch')
    await ctx.send('autotune off, that was dope')

@bot.command(name='bane')
async def bane(ctx):
    playsound('./soundboard/alerts/effect/bane.mp3')
    await autotune_request('Bane')
    await ctx.send('autotune off that was fun')

@bot.command(name='flip')
async def flip(ctx):
    await flip_request()
    await ctx.send('alright eleven, get out of the upside down')

@bot.command(name='friendly')
async def friendly(ctx):
    #playsound('./soundboard/alerts/effect/bane.mp3')
    #await autotune_request('Bane')

    callouts = [gif[:-4] for gif in os.listdir('./soundboard/alerts/friendly') if gif[-4:] == '.txt']

    playsound('./soundboard/{}.mp3'.format(random.choice(callouts)))
    await ctx.send(f'yeah @{ctx.author.name} let\'s play. first game is three innings. My PSN is @Jetsweep30')



@bot.command(name='add')
async def add(ctx):

    sound_info = ctx.content.split(" ")
    sound_name = sound_info[1].lower()

    if sound_name[0] == '@':
        sound_name = sound_name[1:]

    #should people be able to overwrite sounds?
    '''if os.path.isfile('./soundboard/{}.mp3'.format(sound_name)): #1 == 0
        await ctx.send('file "{}.mp3" already exists, use !addf to overwrite'.format(sound_name))
    else:'''

    sound_url = sound_info[2]
    #if it's a giphy download the gif
    if re.search('giphy.com|gph.is', sound_url):
        try:
            gif_url = requests.get(sound_url).url
            await get_gif_from_giphy(gif_url=gif_url, gif_name=sound_name)
            await ctx.send('success! thanks {} for adding gif "!{}"'.format(ctx.author.name, sound_name))
        except:
            try:
                await ctx.send('couldn\'t add gif...')
                time.sleep(1.2)
                await ctx.send('!add [name] [url]')
                time.sleep(1.3)
                await ctx.send('for example... !add jets https://giphy.com/gifs/moodman-TkqchactPDugBnOhWx')
            except:
                pass


    else:
        try:

            sound_start = sound_info[3]
            sound_volume = .12
            try:
                sound_length = min(int(sound_info[4]), 30)
            except:
                sound_length = 7
            sound_effect.do_all(name=sound_name, url=sound_url, start=sound_start, length=sound_length, volume=sound_volume)
            await ctx.send('nice! thanks {} for adding the sound "!{}"'.format(ctx.author.name, sound_name))
            if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
                playsound('./soundboard/{}.mp3'.format(sound_name))
        except:
            pass
            #await ctx.send('didn\'t work try this format...')
            #time.sleep(1.2)
            #await ctx.send('!add [name] [url] [start_time]')
            #time.sleep(1.3)
            #await ctx.send('for example... !add jets 7sllUioMHJY 1:03')

@bot.command(name='help')
async def help(ctx):
    await ctx.send('!add [name] [url] [start_time]')
    time.sleep(1.3)
    await ctx.send(f'for example... !add {ctx.author.name} 7sllUioMHJY 1:03')

# play a random gif from the triggerfyre obs intergration
@bot.command(name='gif')
async def gif(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        gifs = [gif[:-4] for gif in os.listdir('./gifs') if gif[-4:] == '.gif']
        await ctx.channel.send('!' + random.choice(gifs))

# play a random sound from the /soundboard
@bot.command(name='sound')
async def sound(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        sounds = [sound[:-4] for sound in os.listdir('./soundboard') if sound[-4:] == '.mp3']
        await ctx.channel.send('!' + random.choice(sounds))

@bot.command(name='sequence', aliases=['seq' , 'seq3', 'seq4', 'seq5'])
async def sequence(ctx):
    #command = '!seq    4'
    #
    slength = 4
    if ctx.content[:9] == '!sequence':
        slength = 9

    try:
        num_pitches = int(ctx.content[slength:])
    except:
        print('error')
        num_pitches = 4

    await ctx.channel.send("".join([str(random.choice(range(1,num_pitches+1))) for i in range(4)]) + " " + "".join([str(random.choice(range(1,num_pitches+1))) for i in range(4)]))
    #sounds = [sound[:-4] for sound in os.listdir('./soundboard') if sound[-4:] == '.mp3']
    #await ctx.channel.send('!' + random.choice(sounds))



# fix the message so multiple things can happen
'''async def play_the_sound(path):'''

# alerts
@bot.command(name='alert')
async def alert(ctx):
    alert_info = ctx.content.split(" ")
    alert_type = alert_info[1].lower()[:-1]
    #print(alert_type)
    if ctx.author.name in mods and not_live_sports_mode:
        try:
            #print('yeah')
            sounds = [sound[:-4] for sound in os.listdir('./soundboard/alerts/{}'.format(alert_type)) if sound[-4:] == '.mp3']
            await playsound('./soundboard/alerts/{}/{}.mp3'.format(alert_type, random.choice(sounds)))

            if alert_type == 'megaraid':
                global allow_new_intro
                allow_new_intro = False
            else:
                pass
            if alert_type == 'follow':
                make_request(gif_pic = content)
                with open('media/new_follower.txt', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=['new'])
                    #follow_alert = '!alert follow: Thank you for following easy_gaming!'
                    follower_name = alert_info[-1][:-1]
                    writer.writerow({'new': f'new follower: {follower_name}'})
            else:
                pass



        except:
            #print('fail')
            pass
    else:
        pass


# play a random sound from the /soundboard
@bot.command(name='youtube', aliases=['YT' , 'Youtube', 'YouTube', 'yt'])
async def yt(ctx):
    await ctx.channel.send('https://www.youtube.com/channel/UCNJ4U-k24e3qIZRLOSjJfFA')


# play a random sound from the /soundboard
@bot.command(name='w', aliases=['W', 'win', 'Win', 'gg', 'GG'])
async def w(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        content = [sound[:-4] for sound in os.listdir('./gifs/w') if sound[-4:] == '.mp3']
        await ctx.channel.send('!' + random.choice(content))

@bot.command(name='fail')
async def fail(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        content = [sound[:-4] for sound in os.listdir('./gifs/fail') if sound[-4:] == '.txt']
        await ctx.channel.send('!' + random.choice(content))


@bot.command(name='strikeout', aliases=['k', 'K'])
async def strikeout(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        content = [sound[:-4] for sound in os.listdir('./gifs/strikeout') if sound[-4:] == '.txt']
        await ctx.channel.send('!' + random.choice(content))

@bot.command(name='mj')
async def mj(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        await ctx.channel.send('!mj' + str(random.choice(range(1,6))))


@bot.command(name='rigged')
async def rigged(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        await ctx.channel.send('!rigged' + str(random.choice(range(1,10))))

@bot.command(name='homerun', aliases=['hr', 'HR'])
async def homerun(ctx):
    if (not_live_sports_mode or ctx.author.name == 'jetsweep30'):
        content = [sound[:-4] for sound in os.listdir('./gifs/homerun') if sound[-4:] == '.txt']
        await ctx.channel.send('!' + random.choice(content))

# play a random sound from the /soundboard
@bot.command(name='sound_list')
async def sound_list(ctx):
    sounds = [sound[:-4] for sound in os.listdir('./soundboard') if sound[-4:] == '.mp3']
    sounds.sort()
    await ctx.channel.send(', '.join(sounds))

@bot.command(name='sample')
async def sample(ctx):
    gifs = [gif[:-4] for gif in os.listdir('./gifs') if gif[-4:] == '.gif']
    await ctx.channel.send("here's a sample of the collection... !" + ", !".join(random.sample(gifs,4)))


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




@bot.command(name='submit', aliases=['feedback'])
async def submit(ctx):

    sound_info = ctx.content.split(" ")

    if len(sound_info) < 2:
        await ctx.channel.send('drop your track !submit [song-url]')

    else:
        sound_url = sound_info[1]
        print(sound_url)
        try:
            print(ctx.author.name)
            submit_track.get_submitted_track(name=ctx.author.name, url=sound_url)
            await ctx.channel.send(f'thank you for sharing {ctx.author.name} you are added the queue!')
        except:
            await ctx.channel.send(f'well this is embarrasing {ctx.author.name}, can you try again?')






if __name__ == "__main__":
    bot.run()
