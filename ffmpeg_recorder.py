# coding: utf-8
# pylint: disable=too-many-instance-attributes
# pylint: disable=no-self-use
# pylint: disable=arguments-differ

import logging
import subprocess
import os

from ffmpeg_process import *
from scr_config import *

class FfmpegRecorder(object):

    def __init__(self):
        self._scr_config = ScrConfig()
        self._process = FfmpegProcess()
        self._should_be_running = False

        # always disable aero
        self._scr_config.disable_aero = True

        # set some sensible (or not) defaults
        self.scale = .5
        self.output_file = 'output.mp4'
        self.audio_device = 'virtual-audio-capturer'
        self.video_device = 'screen-capture-recorder'
        self.capture_x = 0
        self.capture_y = 0
        self.capture_width = 800
        self.capture_height = 600
        self.capture_fps = 20

        self.debug_show_video = False
        self.records_dir = self._setup_output_folder()
        logging.info('records dir: %s', self.records_dir)

    @staticmethod
    def _setup_output_folder():
        # create the folder if does not exist yet
        name = 'records'
        records_dir = os.path.join(os.getcwd(), name)

        try:
            os.mkdir(records_dir)
        except OSError as e:
            logging.warning(e)

        # share the folder w/ everyone, readonly
        # this is so that the recorded videos can be later accessed over
        # windows shared folders
        try:
            # test if the folder is already shared
            shares = subprocess.check_output('net share')
            if records_dir in shares:
                logging.info('records dir already shared')
                return records_dir

            # construct net share command-line
            cmdline = 'net share {0}={1} /GRANT:Everyone,READ /UNLIMITED /REMARK:"Records output"' \
                .format(name, records_dir)

            # sudo
            cmdline = 'nircmdc elevate {0}'.format(cmdline)

            logging.info('sharing records folder, cmdline=\'%s\'', cmdline)
            subprocess.call(cmdline, stderr=subprocess.STDOUT)
            return records_dir

        except Exception as e:      # pylint: disable=broad-except
            logging.error('failed to share records folder, %s', e)
            return None


    def _ffmpeg_cmdline(self):
        ffmpeg_loglevel = 'error'

        devices = ''
        if self.audio_device:
            devices += 'audio="{audio_device}"'
        if self.audio_device and self.video_device:
            devices += ':'
        if self.video_device:
            devices += 'video="{video_device}"'

        cmdline_template = 'ffmpeg ' + \
                '-loglevel {loglevel} ' + \
                '-f dshow -i ' + devices + ' ' + \
                '-vf scale=iw*{scale}:-1 ' + \
                '-vcodec libx264 -pix_fmt yuv420p -preset ultrafast ' + \
                '-acodec libmp3lame ' + \
                '-y {output}'

        show_video_template = 'ffmpeg ' + \
                '-loglevel {loglevel} ' + \
                '-f dshow -i ' + devices + ' ' + \
                '-filter_complex [0:v]scale=iw*{scale}:-1,split=2[out1][out2] ' + \
                '-map [out1] -map 0:a ' + \
                '-vcodec libx264 -pix_fmt yuv420p -preset ultrafast ' + \
                '-acodec libmp3lame ' + \
                '-y {output} ' + \
                '-map [out2] -f sdl "DO NOT CLOSE THIS WINDOW ({output})"'

        template = show_video_template if self.debug_show_video \
                                    else cmdline_template

        output = os.path.join(self.records_dir, self.output_file)
        return template.format(audio_device=self.audio_device,
                video_device=self.video_device,
                scale=self.scale,
                output=output,
                loglevel=ffmpeg_loglevel)

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

    @property
    def capture_fps(self):
        return self._scr_config.fps

    @capture_fps.setter
    def capture_fps(self, value):
        self._scr_config.fps = value

    def run(self):
        self._process.cmdline = self._ffmpeg_cmdline()
        self._process.run()
        self._should_be_running = True

    def stop(self):
        self._process.stop()
        self._should_be_running = False

    @property
    def has_crashed(self):
        return not self.running and self._should_be_running

    @property
    def running(self):
        return self._process.running

    def pause(self):
        self._process.pause()

    def unpause(self):
        self._process.unpause()

    @property
    def paused(self):
        return self._process.paused






