# coding: utf-8
# pylint: disable=arguments-differ
# pylint: disable=too-many-instance-attributes

import zmq
import logging

from agent_pb2 import *
from abstract_recorder import *

class RemoteRecorder(object):

    def __init__(self, zctx, remote_address='127.0.0.1', ctrl_port=17267,
            status_port=17268):

        # set up zmq machinery
        self._zsck_ctrl = zctx.socket(zmq.PUSH)
        self._zsck_status = zctx.socket(zmq.SUB)
        self._zsck_status.setsockopt(zmq.SUBSCRIBE, '')

        def make_addr(addr, port):
            return 'tcp://{0}:{1}'.format(addr, port)

        ctrl_address = make_addr(remote_address, ctrl_port)
        status_address = make_addr(remote_address, status_port)

        try:
            logging.info('connecting control socket to \'%s\'', ctrl_address)
            self._zsck_ctrl.connect(ctrl_address)
            logging.info('connecting status socket to \'%s\'', status_address)
            self._zsck_status.connect(status_address)
        except zmq.ZMQError as e:
            logging.error('failed to connect zmq socket, message=\'%s\'', e)

        self._connected = False
        self._status_msg = FfmpegStatus()

    def refresh_status(self):
        events = self._zsck_status.poll(0)
        if not events & zmq.POLLIN:
            return False

        zmsg = self._zsck_status.recv()
        tmp = FfmpegStatus()
        tmp.ParseFromString(zmsg)
        self._status_msg.MergeFrom(tmp)
        logging.debug('recved agent status: %s', tmp)
        return True

    def ping(self):
        self._send_opcode(FfmpegControl.PING)

    @property
    def running(self):
        return self._status_msg.is_recording

    def run(self):
        self._send_opcode(FfmpegControl.RECORD)

    def stop(self):
        self._send_opcode(FfmpegControl.IDLE)

    @property
    def paused(self):
        return self._status_msg.is_paused

    def pause(self):
        self._send_opcode(FfmpegControl.PAUSE)

    def unpause(self):
        self._send_opcode(FfmpegControl.UNPAUSE)

    def shutdown(self):
        self._send_opcode(FfmpegControl.SHUTDOWN)

    @property
    def has_crashed(self):
        return self._status_msg.has_crashed

    def _send_opcode(self, opcode):
        msg = FfmpegControl()
        msg.opcode = opcode
        self._send_ctrl(msg)

    def _send_ctrl(self, msg):
        self._zsck_ctrl.send(msg.SerializeToString())



