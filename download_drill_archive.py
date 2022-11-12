from __future__ import unicode_literals
import youtube_dl

from convert import convert_track
import os

import csv

fieldnames = ['creator', 'title', 'id']
i = 0

def download_track(url):
    global i
    print(i)
    print('hello')
    options = {
      'format': 'bestaudio/best',
      'extractaudio' : True,  # only keep the audio
      #'audioformat' : "mp3",  # convert to mp3
      'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'}],
      'postprocessor-args' : '-ss "30"',
      'prefer_ffmpeg': True,
      'outtmpl': f'drill/drill_{i}.',    # name the file the ID of the video
      'noplaylist' : False,    # only download single song, not playlist
    }  # save file as the YouTube ID
    with youtube_dl.YoutubeDL(options) as ydl:
        print('this is ' + str(i))
        r = ydl.extract_info(url, download=False)
        #print(r)
        #print("%s uploaded by '%s', has views,  likes, and dislikes" % (
        i+=1
        os.rename('drill/drill_0.mp3', f'drill/final_{i}.mp3')
        return 'done'
        #print('now it is 'adff + i)
        #break
    #print(r['title'])
    #with open('drill/drill.csv', 'a', newline='') as csvfile:
    #    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #    writer.writerow({'creator': r['title'], 'title': r['title'], 'id': r['id']})
    return ydl.download([url])

def do_all(url=None, name=None, start=None, length=None, volume=None):

    download_track('https://www.youtube.com/watch?v=fcWr1Bd0Vuk&list=PL2wygMju_Tk1VDZQZRNuel_xcG_SQVv5E')
    #convert_track(start=start, length=length, output_name=name, output_volume=volume)

    return 'done'

if __name__ == '__main__':
    do_all()
