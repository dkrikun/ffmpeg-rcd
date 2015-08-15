# coding: utf-8

import time
import msvcrt
import zmq

from agent_pb2 import *

zctx = zmq.Context()
zsck_ctrl = zctx.socket(zmq.PUSH)
zsck_status = zctx.socket(zmq.SUB)
zsck_status.setsockopt(zmq.SUBSCRIBE, '')

zsck_ctrl.connect('tcp://127.0.0.1:17267')
zsck_status.connect('tcp://127.0.0.1:17268')

j = 0
while True:
    cmd = msvcrt.getch() if msvcrt.kbhit() else 0

    msg = FfmpegControl()
    if cmd == 'r':
        msg.opcode = FfmpegControl.RECORD
        zsck_ctrl.send(msg.SerializeToString())
    elif cmd == 't':
        msg.opcode = FfmpegControl.IDLE
        zsck_ctrl.send(msg.SerializeToString())
    elif cmd == 'p':
        msg.opcode = FfmpegControl.PAUSE
        zsck_ctrl.send(msg.SerializeToString())
    elif cmd == 'P':
        msg.opcode = FfmpegControl.UNPAUSE
        zsck_ctrl.send(msg.SerializeToString())
    elif cmd == 'X':
        msg.opcode = FfmpegControl.SHUTDOWN
        zsck_ctrl.send(msg.SerializeToString())

    try:
        zmsg = zsck_status.recv(zmq.NOBLOCK)
        status = FfmpegStatus()
        status.ParseFromString(zmsg)
        print j, status
        j = j + 1

    except zmq.ZMQError as e:
        if e.errno != zmq.EAGAIN:
            raise

    time.sleep(.1)




