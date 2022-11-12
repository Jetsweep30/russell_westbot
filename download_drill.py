from __future__ import unicode_literals
import youtube_dl

from convert import convert_track
import os

import csv
import pandas as pd

fieldnames = ['creator', 'title', 'id']

songs_already_df = pd.read_csv('drill/drill.csv')
songs_already_downloaded = list(songs_already_df['id'])

def get_song_ids_from_playlist(url):

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
      'outtmpl': f'drill/drill.mp3',    # name the file the ID of the video
      'noplaylist' : False,    # only download single song, not playlist
    }  # save file as the YouTube ID
    with youtube_dl.YoutubeDL(options) as ydl:
        r = ydl.extract_info(url, download=False)
        print(r)
        #print(r)
        #print("%s uploaded by '%s', has views,  likes, and dislikes" % (
        #i+=1
        #os.rename('drill/drill_0.mp3', f'drill/final_{i}.mp3')
        #print('now it is 'adff + i)
        #break
    #print(r['title'])
    #with open('drill/drill.csv', 'a', newline='') as csvfile:
    #    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #    writer.writerow({'creator': r['title'], 'title': r['title'], 'id': r['id']})
    #return ydl.download([url])
    song_list = [{'song_id': song['id'], 'artist': song['uploader'],  'title': song['title']} for song in r['entries'] if song['id'] not in songs_already_downloaded]
    return song_list

def download_song(song):

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
      'outtmpl': f'drill/final/{song["title"]}.',    # name the file
      'noplaylist' : True,    # only download single song, not playlist
    }  # save file as the YouTube ID

    url =  f'https://www.youtube.com/watch?v={song["song_id"]}'
    with youtube_dl.YoutubeDL(options) as ydl:
        r = ydl.extract_info(url, download=False)


    return ydl.download([url])

    return 'done'


def do_all(url=None, name=None, start=None, length=None, volume=None):

    #playlist = 'https://www.youtube.com/watch?v=fcWr1Bd0Vuk&list=PL2wygMju_Tk1VDZQZRNuel_xcG_SQVv5E'
    playlist = 'https://www.youtube.com/watch?v=4Hdo4OsODgk&list=PL2wygMju_Tk12vfUxMmbpE1OTJC1CI9JU'
    song_ids = get_song_ids_from_playlist(playlist)

    print(song_ids)
    #return song_ids

    for song in song_ids:

        try:
            download_song(song)

            with open('drill/drill.csv', 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'creator': song['artist'], 'title': song['title'], 'id': song['song_id']})
        except:
            print('FAILURE ')
    return 'done'
    #convert_track(start=start, length=length, output_name=name, output_volume=volume)


if __name__ == '__main__':
    do_all()
