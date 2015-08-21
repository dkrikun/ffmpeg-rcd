# coding: utf-8
# pylint: disable=arguments-differ
# pylint: disable=too-many-instance-attributes

import zmq
import logging
import time

from agent_pb2 import *

class RemoteRecorder(object):

    def __init__(self, zctx, remote_address='127.0.0.1', ctrl_port=17267,
            status_port=17268):

        # initialize connection defaults
        self._remote_address = remote_address
        self._ctrl_port = ctrl_port
        self._status_port = status_port

        # set up zmq machinery
        self._zsck_ctrl = zctx.socket(zmq.PUSH)
        self._zsck_status = zctx.socket(zmq.SUB)
        self._zsck_status.setsockopt(zmq.SUBSCRIBE, '')

        # connect using defaults
        self._connected = False
        self.connect()

        self._status_msg = FfmpegStatus()
        self._status_timestamp = 0.

    def connect(self):
        if not self._connected:
            self._connect_sock(self._zsck_ctrl, self.ctrl_address)
            self._connect_sock(self._zsck_status, self.status_address)
            self._connected = True

        self.ping()

    def disconnect(self):
        if self._connected:
            self._zsck_ctrl.disconnect(self.ctrl_address)
            self._zsck_status.disconnect(self.status_address)
            self._connected = False

    @property
    def connected(self):
        return self._connected

    @property
    def remote_address(self):
        return self._remote_address

    @remote_address.setter
    def remote_address(self, value):
        self._remote_address = value

    @property
    def ctrl_port(self):
        return self._ctrl_port

    @ctrl_port.setter
    def ctrl_port(self, value):
        self._ctrl_port = value

    @property
    def ctrl_address(self):
        return self._make_address(self.remote_address, self.ctrl_port)

    @property
    def status_port(self):
        return self._status_port

    @status_port.setter
    def status_port(self, value):
        self._status_port = value

    @property
    def status_address(self):
        return self._make_address(self.remote_address, self.status_port)

    @staticmethod
    def _make_address(ip, port):
        return 'tcp://{0}:{1}'.format(ip, port)

    @staticmethod
    def _connect_sock(zsck, address):
        try:
            logging.info('connecting to \'%s\'..', address)
            zsck.connect(address)
        except zmq.ZMQerror as e:
            logging.error('connection failed, message=\'%s\'', e)

    def refresh_status(self):
        # check if there is an incoming status message available
        events = self._zsck_status.poll(0)
        if not events & zmq.POLLIN:
            return False

        # recv zmq message
        zmsg = self._zsck_status.recv()
        self._status_timestamp = time.time()

        # use temp. protobuf message so that we can merge it w/ the one stored
        # internally; this is because the status updates are usually incremental
        tmp = FfmpegStatus()
        tmp.ParseFromString(zmsg)
        logging.debug('recved status:\n%s', tmp)

        self._status_msg.MergeFrom(tmp)
        return True

    @property
    def status_at(self):
        return self._status_timestamp

    @property
    def status_before(self):
        return time.time() - self._status_timestamp

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
        events = self._zsck_ctrl.poll(1, zmq.POLLOUT)
        if events & zmq.POLLOUT:
            self._zsck_ctrl.send(msg.SerializeToString())



