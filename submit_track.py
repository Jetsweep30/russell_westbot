from __future__ import unicode_literals
import youtube_dl

from convert import convert_track
import re



def download_track(url, name):

    options1 = {
      'format': 'bestaudio/best',
      'extractaudio' : True,  # only keep the audio
      #'audioformat' : "mp3",  # convert to mp3
      'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'}],
      'postprocessor-args' : '-ss "30"',
      'prefer_ffmpeg': True,
      'outtmpl': f'drill/queue/{name}.',    # name the file the ID of the video
      'noplaylist' : True,    # only download single song, not playlist
    }  # save file as the YouTube ID
    with youtube_dl.YoutubeDL(options1) as ydl1:
        r = ydl1.extract_info(url, download=False)
        #re.sub(r'[^ \w+]', '', name)
        try:
            track_name = name + ' - ' +  re.sub(r'[^ \w+]', '', r['title'])
        except:
            track_name = name + '- Unknown Track'



    options = {
      'format': 'bestaudio/best',
      'extractaudio' : True,  # only keep the audio
      #'audioformat' : "mp3",  # convert to mp3
      'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'}],
      'postprocessor-args' : '-ss "30"',
      'prefer_ffmpeg': True,
      'outtmpl': f'drill/queue/{track_name}.',    # name the file the ID of the video
      'noplaylist' : True,    # only download single song, not playlist
    }  # save file as the YouTube ID
    with youtube_dl.YoutubeDL(options) as ydl:
        r = ydl.extract_info(url, download=False)
        #print(r['title'])
        #re.sub(r'[^ \w+]', '', name)
    ydl.download([url])


    return 'done'


def get_submitted_track(url=None, name=None, start=None, length=None, volume=None):

    download_track(url, name)

    return 'done'

if __name__ == '__main__':
    get_submitted_track()
