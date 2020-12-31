
import os
#import sys
import re


def convert_track(start = 0, length = 7, output_name='default', output_volume=0.12):


    command = f"ffmpeg -ss {start} -t {length} -i soundboard/staging/staging.mp3 -vn -ar 44100 -ac 2 -b:a 192k -filter_complex alimiter=level_in=1:level_out=1:limit={output_volume}:attack=7:release=100:level=disabled -y soundboard/{output_name}.mp3"
    return os.system(command)




'''-ss HH:MM:SS : start time to take
-to HH:MM:SS : end time
-t HH:MM:SS : time length to take


ffmpeg -ss 45 -t 6 -i gxIEt3KEohk.mp3 gxIEt3KEohk.ogg
'''

async def get_gif_from_giphy(gif_url=None, gif_name=None):

    #gif_url = 'https://giphy.com/gifs/trash-100soft-intensifies-hpRlrdtjCuh1IVvfSv'
    gif_url = re.sub('/links', '', gif_url)
    gif_id = re.split('-|/',gif_url)[-1] #.split('-')


    command = f"curl https://i.giphy.com/media/{gif_id}/giphy.gif --output gifs/{gif_name}.gif"

    return os.system(command)

if __name__ == '__main__':
    convert_track()
