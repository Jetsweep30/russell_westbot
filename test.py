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

import time

import random

alert_info = '!alert follow nice'.split(" ")
alert_type = 'follow'


sounds = [sound[:-4] for sound in os.listdir('./soundboard/alerts/{}'.format(alert_type)) if sound[-4:] == '.mp3']
print(sounds)
playsound('./soundboard/alerts/{}/{}.mp3'.format(alert_type, random.choice(sounds)))
print('what')
if alert_type == 'megaraid':
    global allow_new_intro
    allow_new_intro = False
else:
    pass

if alert_type == 'follow':
    print('yes')
