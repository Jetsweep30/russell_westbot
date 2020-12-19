from __future__ import unicode_literals
import youtube_dl

from convert import convert_track

def download_track(url):
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
      'outtmpl': 'soundboard/staging/staging.',    # name the file the ID of the video
      'noplaylist' : True,    # only download single song, not playlist
    }  # save file as the YouTube ID
    with youtube_dl.YoutubeDL(options) as ydl:
        r = ydl.extract_info(url, download=False)
        #print(r)
        print("%s uploaded by '%s', has %d views, %d likes, and dislikes" % (
        r['title'], r['uploader'], r['view_count'], r['like_count']))
    return ydl.download([url])

def do_all(url=None, name=None, start=None, length=None, volume=None):

    download_track(url)
    convert_track(start=start, length=length, output_name=name, output_volume=volume)

    return 'done'

if __name__ == '__main__':
    do_all()
