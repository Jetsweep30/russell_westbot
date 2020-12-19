
import os
#import sys


def convert_track(start = 0, length = 7, output_name='default', output_volume=0.06):


    command = f"ffmpeg -ss {start} -t {length} -i soundboard_staging/staging.mp3 -vn -ar 44100 -ac 2 -b:a 192k -filter:a \"volume={output_volume}\" -y soundboard/{output_name}.mp3"
    return os.system(command)


'''-ss HH:MM:SS : start time to take
-to HH:MM:SS : end time
-t HH:MM:SS : time length to take


ffmpeg -ss 45 -t 6 -i gxIEt3KEohk.mp3 gxIEt3KEohk.ogg
'''

if __name__ == '__main__':
    convert_track()
