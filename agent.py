# coding: utf-8

__version__ = '0.1.0'
__author__ = 'Daniel Krikun'
__license__ = 'MIT'

import sys
import logging
import msvcrt
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
    prsr.add_argument('--ctrl-address', help='remote control address')
    prsr.add_argument('--status-address', help='status address')
    prsr.add_argument('--frequency', help='main loop frequency')
    prsr.add_argument('--nostdin', action='store_true',
            help='disable kbhit control')

    prsr.add_argument('--show-video', action='store_true',
            help='show the recorded video in a window')

    return prsr.parse_args()

# pylint: disable=too-many-branches,too-many-statements,too-many-locals
def main():
    """Main here."""

    args = parse_cmdline_args()

    # decide on logging severity level
    severity_level = logging.ERROR if args.silent else logging.DEBUG \
            if args.verbose else logging.INFO

    # set up logging
    logging.basicConfig(stream=sys.stderr, level=severity_level,
            format='%(message)s')

    # debug-print the parsed arguments
    logging.debug(args)

    # debug-print zmq version info
    logging.info('zmq version=%s', zmq.zmq_version())
    logging.info('pyzmq version=%s', zmq.pyzmq_version())

    # set up zmq machinery
    zctx = zmq.Context()
    zsck_ctrl = zctx.socket(zmq.PULL)

    ctrl_addr = args.ctrl_address or 'tcp://*:17267'
    zsck_ctrl.bind(ctrl_addr)

    zsck_status = zctx.socket(zmq.PUB)
    status_addr = args.status_address or 'tcp://*:17268'
    zsck_status.bind(status_addr)

    recorder = FfmpegRecorder()
    recorder.debug_show_video = args.show_video

    # main loop frequency
    frequency = args.frequency or 30.

    # last status, to send messages on change only
    recording = recorder.running
    paused = recorder.paused
    has_crashed = recorder.has_crashed

    # whether full status has been requested, initially true
    status_requested = True

    should_stop = False
    while not should_stop:

        # check if an incoming message is available
        events = zsck_ctrl.poll(1000./frequency)

        if events & zmq.POLLIN:
            zmsg = zsck_ctrl.recv()
            msg = FfmpegControl()
            msg.ParseFromString(zmsg)
            logging.debug('recved ctrl:\n%s', msg)

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
                should_stop = True

            elif msg.opcode == FfmpegControl.PING:
                status_requested = True

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
                recorder.capture_fps = msg.capture_fps

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

            elif cmd == 'i':
                status_requested = True

            elif cmd == 'X':
                recorder.stop()
                should_stop = True

        # send full status on shutdown
        if should_stop:
            status_requested = True

        # publish status
        status = FfmpegStatus()
        dirty = False

        if recorder.running != recording:
            recording = recorder.running
            status.is_recording = recorder.running
            dirty = True

        if recorder.paused != paused:
            paused = recorder.paused
            status.is_paused = recorder.paused
            dirty = True

        if recorder.has_crashed != has_crashed:
            has_crashed = recorder.has_crashed
            status.has_crashed = recorder.has_crashed
            dirty = True

        # whether status message has been requested explicitly
        if status_requested:
            status.is_recording = recorder.running
            status.is_paused = recorder.paused
            status.has_crashed = recorder.has_crashed
            status_requested = False
            dirty = True

        if dirty:
            logging.debug('sending status:\n%s', status)
            events = zsck_status.poll(0, zmq.POLLOUT)

            # TODO what if we can't send? the message will be dropped!
            if events & zmq.POLLOUT:
                zsck_status.send(status.SerializeToString())

if __name__ == "__main__":
    sys.exit(main())

