from PySide import QtCore, QtGui
import sys
import logging
import zmq
from remote_recorder import RemoteRecorder

from rx.subjects import Subject
from rx.concurrency import QtScheduler

class RemoteControl(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RemoteControl, self).__init__(parent)

        # set up zmq and model
        self._zctx = zmq.Context()
        self._model = RemoteRecorder(self._zctx)

        # setup a timer to check for incoming messages
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._refresh_model_status)
        self._timer.start(33)

        # setup a timer to ping for connection
        self._ping_period = 2000
        self._ping = QtCore.QTimer(self)
        self._ping.timeout.connect(self._ping_model)
        self._ping.start(self._ping_period)

        self.setWindowTitle('Remote Control')

        layout = QtGui.QVBoxLayout()

        self._remote_address = QtGui.QLineEdit(self._model.remote_address)
        layout.addWidget(self._remote_address)

        self._ctrl_port = QtGui.QLineEdit(str(self._model.ctrl_port))
        layout.addWidget(self._ctrl_port)

        self._status_port = QtGui.QLineEdit(str(self._model.status_port))
        layout.addWidget(self._status_port)

        self._connected = QtGui.QCheckBox('connected?')
        layout.addWidget(self._connected)

        self._connect = QtGui.QPushButton('Connect')
        self._connect.clicked.connect(self._connect_model)
        layout.addWidget(self._connect)

        self._disconnect = QtGui.QPushButton('Disconnect')
        self._disconnect.clicked.connect(self._model.disconnect)
        layout.addWidget(self._disconnect)

        self._record = QtGui.QPushButton('Record')
        self._record.clicked.connect(self._model.run)
        layout.addWidget(self._record)

        self._stop = QtGui.QPushButton('Stop')
        self._stop.clicked.connect(self._model.stop)
        layout.addWidget(self._stop)

        self._pause = QtGui.QPushButton('Pause')
        self._pause.clicked.connect(self._model.pause)
        layout.addWidget(self._pause)

        self._unpause = QtGui.QPushButton('Unpause')
        self._unpause.clicked.connect(self._model.unpause)
        layout.addWidget(self._unpause)

        self._shutdown = QtGui.QPushButton('Shutdown')
        self._shutdown.clicked.connect(self._model.shutdown)
        layout.addWidget(self._shutdown)

        self._running = QtGui.QCheckBox('running?')
        layout.addWidget(self._running)

        self._paused = QtGui.QCheckBox('paused?')
        layout.addWidget(self._paused)

        self._has_crashed = QtGui.QCheckBox('has crashed?')
        layout.addWidget(self._has_crashed)

        self._responding = QtGui.QCheckBox('responding?')
        layout.addWidget(self._responding)

        self.setLayout(layout)
        self.show()

        self._model.connected_sbj.subscribe(lambda x: self._connected.setChecked(x))

    def _refresh_model_status(self):
        if self._model.refresh_status():

            # update view
            self._running.setChecked(self._model.running)
            self._paused.setChecked(self._model.paused)
            self._has_crashed.setChecked(self._model.has_crashed)

            # mark as responding
            self._responding.setChecked(True)

    def _ping_model(self):
        # request explicit status message
        logging.debug('pinging..')
        self._model.ping()

        # check when the last status message has been recved
        logging.debug('status recved before %.2f sec.', \
                self._model.status_before)

        thresh_factor = 1.5
        status_before_msec = 1e3*self._model.status_before
        is_responding = status_before_msec < thresh_factor * self._ping_period
        self._responding.setChecked(is_responding)

    def _connect_model(self):
        self._model.remote_address = self._remote_address.text()
        self._model.ctrl_port = int(self._ctrl_port.text())
        self._model.status_port = int(self._status_port.text())
        self._model.connect()


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
            format='%(message)s')

    app = QtGui.QApplication(sys.argv)
    scheduler = QtScheduler(QtCore)

    window = RemoteControl()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())


