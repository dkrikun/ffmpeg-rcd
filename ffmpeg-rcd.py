# coding: utf-8

__version__ = '0.1.0'
__author__ = 'Daniel Krikun'
__license__ = 'MIT'

import sys
import logging
import psutil
from subprocess import PIPE

class FfmpegProcess:
    def __init__(self, cmdline):
        self._cmdline = cmdline
        self._paused = False
        self._process = None

    def run(self):
        if not self.running:
            logging.debug('starting ffmpeg with command-line:\n`{0}`'
                    .format(self._cmdline))

            # stdin pipe is required to shutdown ffmpeg gracefully (see below)
            self._process = psutil.Popen(self._cmdline, stdin=PIPE)

    def stop(self):
        if self.paused:
            self.unpause()

        if self.running:
            logging.debug('stopping ffmpeg process')

            # emulate 'q' keyboard press
            self._process.communicate(input='q')
            self._process.wait()

    @property
    def running(self):
        return self._process is not None and self._process.is_running()

    def pause(self):
        if self.running:
            if not self._paused:
                logging.debug('suspending ffmpeg process')

                self._process.suspend()
                self._paused = True

    def unpause(self):
        if self.running:
            if self._paused:
                logging.debug('resuming ffmpeg process')

                self._process.resume()
                self._paused = False

    @property
    def paused(self):
        return self._paused

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
            format='%(message)s')

    import msvcrt
    import time

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

