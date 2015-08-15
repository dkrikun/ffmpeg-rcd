# coding: utf-8

from abc import *

class AbstractRecorder(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def capture_x(self):
        pass

    @capture_x.setter
    def capture_x(self, value):
        pass

    @abstractproperty
    def capture_y(self):
        pass

    @capture_y.setter
    def capture_y(self, value):
        pass

    @abstractproperty
    def capture_width(self):
        pass

    @capture_width.setter
    def capture_width(self, value):
        pass

    @abstractproperty
    def capture_height(self):
        pass

    @capture_height.setter
    def capture_height(self, value):
        pass

    @abstractproperty
    def capture_fps(self):
        pass

    @capture_fps.setter
    def capture_fps(self, value):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractproperty
    def has_crashed(self):
        pass

    @abstractproperty
    def running(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def unpause(self):
        pass

    @abstractproperty
    def paused(self):
        pass







