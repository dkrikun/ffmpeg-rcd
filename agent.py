# coding: utf-8

__version__ = '0.1.0'
__author__ = 'Daniel Krikun'
__license__ = 'MIT'

import sys
import logging
import msvcrt
import time
from argparse import ArgumentParser
import zmq

from agent_pb2 import *
from ffmpeg_recorder import *

def parse_cmdline_args():
    """Parse command-line arguments."""

    prsr = ArgumentParser(description='Distributed screen recorder agent')
    prsr.add_argument('--version', action='version',
            version='%(prog)s {}'.format(__version__))

    verbosity_group = prsr.add_mutually_exclusive_group()
    verbosity_group.add_argument('-V', '--verbose', action='store_true',
                                 help='be verbose')
    verbosity_group.add_argument('-q', '--silent', action='store_true',
                                 help='be silent')
    prsr.add_argument('--address', help='remote control address')
    prsr.add_argument('--nostdin', action='store_true',
            help='disable kbhit control')

    prsr.add_argument('--show-video', action='store_true',
            help='show the recorded video in a window')

    prsr.add_argument('--output-file', help='output video file')

    return prsr.parse_args()

def main():
    """Main here."""

    args = parse_cmdline_args()

    # decide on logging severity level
    severity_level = logging.CRITICAL if args.silent else logging.DEBUG \
            if args.verbose else logging.INFO

    # set up logging
    logging.basicConfig(stream=sys.stderr, level=severity_level,
            format='%(message)s')

    # debug-print the parsed arguments
    logging.debug(args)

    # set up zmq machinery
    zctx = zmq.Context()
    zsck_ctrl = zctx.socket(zmq.PULL)
    zpoll = zmq.Poller()
    zpoll.register(zsck_ctrl, zmq.POLLIN)

    ctrl_addr = args.address or 'tcp://*:7267'
    zsck_ctrl.bind(ctrl_addr)

    recorder = FfmpegRecorder()
    recorder.debug_show_video = args.show_video
    recorder.output_file = args.output_file or 'output.mp4'

    # main loop frequency
    frequency = 30.;

    while True:
        # check if an incoming message is available
        ready_socks = dict(zpoll.poll(1./frequency))

        if zsck_ctrl in ready_socks:
            zmsg = zsck_ctrl.recv(zmq.NOBLOCK)
            msg.ParseFromString(zmsg)
            logging.debug('recved: %s', msg)

            if msg.opcode == FfmpegControl.RECORD:
                recorder.run()

            elif msg.opcode == FfmpegControl.IDLE:
                recorder.stop()

            elif msg.opcode == FfmpegControl.PAUSE:
                recorder.pause()

            elif msg.opcode == FfmpegControl.UNPAUSE:
                recorder.unpause()

            elif msg.opcode == FfmpegControl.SHUTDOWN:
                recorder.stop()
                break

            # update recording parameters
            if msg.HasField('capture_x'):
                recorder.capture_x = msg.capture_x

            if msg.HasField('capture_y'):
                recorder.capture_y = msg.capture_y

            if msg.HasField('capture_width'):
                recorder.capture_width = msg.capture_width

            if msg.HasField('capture_height'):
                recorder.capture_height = msg.capture_height

            if msg.HasField('capture_fps'):
                recorder.fps = msg.capture_fps

            if msg.HasField('audio_device'):
                recorder.audio_device = msg.audio_device

            if msg.HasField('video_device'):
                recorder.video_device = msg.video_device

            if msg.HasField('scale'):
                recorder.scale = msg.scale

            if msg.HasField('output_file'):
                recorder.output_file = msg.output_file

            if msg.HasField('debug_show_video'):
                recorder.debug_show_video = msg.debug_show_video

        # dispatch kbhit commands
        if not args.nostdin:
            cmd = msvcrt.getch() if msvcrt.kbhit() else 0

            if cmd == 'r':
                recorder.run()

            elif cmd == 't':
                recorder.stop()

            elif cmd == 'p':
                recorder.pause()

            elif cmd == 'P':
                recorder.unpause()

            elif cmd == 'X':
                recorder.stop()
                break

if __name__ == "__main__":
    sys.exit(main())

