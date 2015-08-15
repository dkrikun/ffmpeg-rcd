# coding: utf-8
# pylint: disable=arguments-differ
# pylint: disable=too-many-instance-attributes

import zmq
import logging

from agent_pb2 import *
from abstract_recorder import *

class RemoteRecorder(AbstractRecorder):

    def __init__(self, zctx, remote_address='127.0.0.1', control_port=17267,
            status_port=17268):

        self.zsck_ctrl = zctx.socket(zmq.PUSH)
        self.zsck_status = zctx.socket(zmq.SUB)
        self.zsck_status.setsockopt(zmq.SUBSCRIBE, '')

        ctrl_address = remote_address + str(control_port)
        status_address = remote_address + str(status_port)

        try:
            logging.info('connecting control socket to \'%s\'', ctrl_address)
            self.zsck_ctrl.connect(ctrl_address)
            logging.info('connecting status socket to \'%s\'', status_address)
            self.zsck_status.connect(status_address)
        except zmq.ZMQError as e:
            logging.error('failed to connect zmq socket, message=\'%s\'', e)



