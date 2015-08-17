from PySide import QtCore, QtGui
import sys
import logging
import zmq
from remote_recorder import RemoteRecorder

class RemoteControl(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RemoteControl, self).__init__(parent)

        # set up zmq and model
        self._zctx = zmq.Context()
        self._model = RemoteRecorder(self._zctx)

        # setup a timer to check for incoming messages
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._refresh_model)
        self._timer.start(33)

        # setup a timer to ping for connection
        self._ping = QtCore.QTimer(self)
        self._ping.timeout.connect(self._ping_model)
        self._ping.start(1000)

        self.setWindowTitle('Remote Control')

        layout = QtGui.QVBoxLayout()

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

        self._last_updated = QtGui.QLabel('')
        layout.addWidget(self._last_updated)

        self.setLayout(layout)
        self.show()

    def _refresh_model(self):
        if self._model.refresh_status():
            self._running.setChecked(self._model.running)
            self._paused.setChecked(self._model.paused)
            self._has_crashed.setChecked(self._model.has_crashed)
            self._last_updated.setText(str(self._model.status_at))
            self._last_updated.adjustSize()

    def _ping_model(self):
        self._model.ping()

def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
            format='%(message)s')

    app = QtGui.QApplication(sys.argv)
    window = RemoteControl()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())


