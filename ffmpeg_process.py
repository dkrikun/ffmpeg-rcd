# coding: utf-8

import logging
import psutil
from subprocess import PIPE

class FfmpegProcess(object):
    def __init__(self):
        self._cmdline = None
        self._process = None
        self._paused = False

    def run(self):
        if not self._cmdline:
            logging.debug('cmdline is not yet defined')
            return

        if not self.running:
            logging.debug('starting ffmpeg with command-line:\n`%s`',
                    self.cmdline)

            # stdin pipe is required to shutdown ffmpeg gracefully (see below)
            self._process = psutil.Popen(self._cmdline, stdin=PIPE)

    def stop(self):
        if self.running:
            logging.debug('stopping ffmpeg process')

            self._process.resume()
            # emulate 'q' keyboard press to shutdown ffmpeg
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
        return self._paused and self.running

    @property
    def cmdline(self):
        return self._cmdline

    @cmdline.setter
    def cmdline(self, value):
        self._cmdline = value

