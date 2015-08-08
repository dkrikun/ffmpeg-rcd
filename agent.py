# coding: utf-8

__version__ = '0.1.0'
__author__ = 'Daniel Krikun'
__license__ = 'MIT'

import sys
import logging
import msvcrt
import time

from ffmpeg_recorder import *

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
            format='%(message)s')

    ffmpeg_recorder = FfmpegRecorder()

    cmd = 0
    while True:
        time.sleep(33./1000.)

        if not msvcrt.kbhit():
            continue

        cmd = msvcrt.getch()
        if cmd == 'r':
            ffmpeg_recorder.run()

        elif cmd == 's':
            ffmpeg_recorder.stop()

        elif cmd == 'p':
            ffmpeg_recorder.pause()

        elif cmd == 'Q':
            ffmpeg_recorder.stop()
            break

if __name__ == "__main__":
    sys.exit(main())

