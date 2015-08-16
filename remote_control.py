from PySide import QtCore, QtGui
import sys
import logging
import zmq
from remote_recorder import RemoteRecorder

class RemoteControl(QtGui.QWidget):
    def __init__(self, parent=None):
        super(RemoteControl, self).__init__(parent)

        self._zctx = zmq.Context()
        self._model = RemoteRecorder(self._zctx)

        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._refresh_model)
        self._timer.start(1)

        self.setGeometry(300, 300, 250, 150)
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

        self.setLayout(layout)

        self.show()

    def _refresh_model(self):
        self._model.refresh()



def main():
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
            format='%(message)s')

    app = QtGui.QApplication(sys.argv)
    window = RemoteControl()
    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())


