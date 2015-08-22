# coding: utf-8

import zmq
import sys
import time
import numpy as np
import cv2

from agent_pb2 import *
from image_generator import *

def main():
    # set up zmq machinery
    zctx = zmq.Context()
    zsck_status = zctx.socket(zmq.SUB)
    zsck_status.setsockopt(zmq.SUBSCRIBE, '')

    status_address = 'tcp://127.0.0.1:17268'
    zsck_status.connect(status_address)

    # set up image generator
    ig = ImageGenerator()

    # loop clock
    frequency = 30.

    # update image each every dt msec.
    dt = 1.
    text_update_timestamp = time.time()

    j = 0
    text = '---'

    recording = False
    start_recording_timestamp = 0.

    while True:
        events = zsck_status.poll(0)
        if events & zmq.POLLIN:
            zmsg = zsck_status.recv()
            msg = FfmpegStatus()
            msg.ParseFromString(zmsg)

            prev_recording = recording
            recording = msg.is_recording

            if recording and not prev_recording:
                start_recording_timestamp = time.time()

        if recording:
            now = time.time()

            # update rendered text
            if now - text_update_timestamp > dt:
                j = (j + 1) % 100
                text = '{iter:03d}'.format(iter=j)
                text_update_timestamp = now

        # always display the image
        image = ig.frame(text)
        cv2.imshow('test', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    sys.exit(main())


