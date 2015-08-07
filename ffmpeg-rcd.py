import psutil
from subprocess import PIPE

class FfmpegProcess:
    def __init__(self, cmdline):
        self._cmdline = cmdline
        self._running = False
        self._paused = False

    def run(self):
        if not self._running:
            # stdin pipe is required to shutdown ffmpeg gracefully (see below)
            self._process = psutil.Popen(self._cmdline, stdin=PIPE)
            self._running = True

    def stop(self):
        if self._running:
            # emulate 'q' keyboard press
            self._process.communicate(input='q')
            self._process.wait()
            self._running = False

    def pause(self):
        if not self._paused:
            self._process.suspend()
            self._paused = True

    def unpause(self):
        if self._paused:
            self._process.resume()
            self._paused = False

    def is_paused(self):
        return self._paused

    def toggle_paused(self):
        if self._paused:
            self.unpause()
        else:
            self.pause()


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
        xx.toggle_paused()


