# coding: utf-8

import logging
from ffmpeg_process import *
from scr_config import *

class FfmpegRecorder(object):

    def __init__(self):
        self._scr_config = ScrConfig()
        self._process = FfmpegProcess()

        # set these screen-capture-recorder settings hardcoded
        self._scr_config.disable_aero = True
        self._scr_config.fps = 20

        # set some sensible (or not) defaults
        self.scale = .5
        self.output_file = 'output.mp4'
        self.audio_device = 'Microphone (High Definition Aud'
        self.video_device = 'screen-capture-recorder'
        self.capture_x = 0
        self.capture_y = 0
        self.capture_width = 800
        self.capture_height = 600

        self.debug_show_video = True

    def _ffmpeg_cmdline(self):
        cmdline_template = 'ffmpeg ' + \
                '-loglevel info ' + \
                '-f dshow -i audio="{0}":video="{1}" ' + \
                '-vf scale=iw*{2}:-1 ' + \
                '-vcodec libx264 -pix_fmt yuv420p -preset ultrafast ' + \
                '-acodec libmp3lame ' + \
                '-y {3}'

        show_video_template = 'ffmpeg ' + \
                '-loglevel info ' + \
                '-f dshow -i audio="{0}":video="{1}" ' + \
                '-filter_complex [0:v]scale=iw*{2}:-1,split=2[out1][out2] ' + \
                '-map [out1] -map 0:a ' + \
                '-vcodec libx264 -pix_fmt yuv420p -preset ultrafast ' + \
                '-acodec libmp3lame ' + \
                '-y {3} ' + \
                '-map [out2] -f sdl "DO NOT CLOSE THIS WINDOW ({3})"'

        template = show_video_template if self.debug_show_video \
                                    else cmdline_template

        return template.format(self.audio_device,
                self.video_device,
                self.scale,
                self.output_file)

    @property
    def capture_x(self):
        return self._scr_config.x

    @capture_x.setter
    def capture_x(self, value):
        self._scr_config.x = value

    @property
    def capture_y(self):
        return self._scr_config.y

    @capture_y.setter
    def capture_y(self, value):
        self._scr_config.y = value

    @property
    def capture_width(self):
        return self._scr_config.width

    @capture_width.setter
    def capture_width(self, value):
        self._scr_config.width = value

    @property
    def capture_height(self):
        return self._scr_config.height

    @capture_height.setter
    def capture_height(self, value):
        self._scr_config.height = value

    def run(self):
        self._process.cmdline = self._ffmpeg_cmdline()
        self._process.run()

    def stop(self):
        self._process.stop()

    @property
    def running(self):
        return self._process.running()

    def pause(self):
        self._process.pause()

    def unpause(self):
        self._process.unpause()

    @property
    def paused(self):
        return self._process.paused







