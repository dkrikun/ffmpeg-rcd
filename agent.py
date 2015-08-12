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

    ctrl_addr = args.address or 'tcp://*:7267'
    zsck_ctrl.bind(ctrl_addr)

    recorder = FfmpegRecorder()
    recorder.debug_show_video = args.show_video
    recorder.output_file = args.output_file or 'output.mp4'

    # main loop frequency
    frequency = 30.;

    while True:
        # FIXME use zmq poll instead of sleep
        time.sleep(1./frequency)

        # check if we have an incoming message
        zmsg = None
        try:
            zmsg = zsck_ctrl.recv(zmq.NOBLOCK)
        except zmq.ZMQError as e:
            if e.errno != zmq.EAGAIN:
                raise

        msg = FfmpegControl()
        if zmsg is not None:
            msg.ParseFromString(zmsg)
            logging.debug('recved: %s', msg)

        # check if a key has been pressed
        cmd = 0 if args.nostdin else \
                msvcrt.getch() if msvcrt.kbhit() else 0

        if msg.opcode == FfmpegControl.RECORD or cmd == 'r':
            recorder.run()

        elif msg.opcode == FfmpegControl.IDLE or cmd == 't':
            recorder.stop()

        elif msg.opcode == FfmpegControl.PAUSE or cmd == 'p':
            recorder.pause()

        elif msg.opcode == FfmpegControl.UNPAUSE or cmd == 'P':
            recorder.unpause()

        elif msg.opcode == FfmpegControl.SHUTDOWN or cmd == 'X':
            recorder.stop()
            break

if __name__ == "__main__":
    sys.exit(main())

