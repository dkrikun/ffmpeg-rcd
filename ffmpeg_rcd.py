# coding: utf-8

__version__ = '0.1.0'
__author__ = 'Daniel Krikun'
__license__ = 'MIT'

import sys
import logging
import msvcrt
import time

from ffmpeg_process import *

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
            format='%(message)s')

    audio_device = 'Microphone (High Definition Aud'
    video_device = 'screen-capture-recorder'
    output = 'output.mp4'

    cmdline_template = 'ffmpeg \
-loglevel fatal \
-f dshow -i audio="{0}":video="{1}" \
-vcodec libx264 -pix_fmt yuv420p -preset ultrafast -acodec libmp3lame \
-y {2}'

    cmdline = cmdline_template.format(audio_device, video_device, output)
    xx = FfmpegProcess(cmdline)


    cmd = 0
    while True:
        time.sleep(33./1000.)
        if not msvcrt.kbhit():
            continue

        cmd = msvcrt.getch()
        if cmd == 'r':
            xx.run()

        elif cmd == 's':
            xx.stop()

        elif cmd == 'p':
            xx.pause()

        elif cmd == '1':
            xx.print_stats()

        elif cmd == 'Q':
            xx.stop()
            break

if __name__ == "__main__":
    sys.exit(main())

