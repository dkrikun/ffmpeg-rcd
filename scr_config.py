# coding: utf-8
# pylint: disable=no-self-use

import logging
import _winreg

class ScrConfig(object):

    # shortcut
    HKCU = _winreg.HKEY_CURRENT_USER

    # registry key containing screen-capture-recorder settings
    PREFIX = r'Software\screen-capture-recorder'

    # screen-capture-recorder registry value names that we want to configure
    X = 'start_x'
    Y = 'start_y'
    WIDTH = 'capture_width'
    HEIGHT = 'capture_height'
    FPS = 'default_max_fps'
    DISABLE_AERO = 'disable_aero_for_vista_plus_if_1'

    # x
    @property
    def x(self):
        return self._get(ScrConfig.X)

    @x.setter
    def x(self, value):
        self._set(ScrConfig.X, value)

    @x.deleter
    def x(self):
        self._del(ScrConfig.X)

    # y
    @property
    def y(self):
        return self._get(ScrConfig.Y)

    @y.setter
    def y(self, value):
        self._set(ScrConfig.Y, value)

    @y.deleter
    def y(self):
        self._del(ScrConfig.Y)

    # width
    @property
    def width(self):
        return self._get(ScrConfig.WIDTH)

    @width.setter
    def width(self, value):
        self._set(ScrConfig.WIDTH, value)

    @width.deleter
    def width(self):
        self._del(ScrConfig.WIDTH)

    @property
    def height(self):
        return self._get(ScrConfig.HEIGHT)

    @height.setter
    def height(self, value):
        self._set(ScrConfig.HEIGHT, value)

    @height.deleter
    def height(self):
        self._del(ScrConfig.HEIGHT)

    @property
    def fps(self):
        return self._get(ScrConfig.FPS)

    @fps.setter
    def fps(self, value):
        self._set(ScrConfig.FPS, value)

    @fps.deleter
    def fps(self):
        self._del(ScrConfig.FPS)

    @property
    def disable_aero(self):
        return self._get(ScrConfig.DISABLE_AERO) != 0

    @disable_aero.setter
    def disable_aero(self, value):
        self._set(ScrConfig.DISABLE_AERO, 1 if value else 0)

    @disable_aero.deleter
    def disable_aero(self):
        self._del(ScrConfig.DISABLE_AERO)

    # read/write to registry
    def _set(self, opt, value):
        logging.debug('setting `%s` to %d', opt, value)

        if value < 0:
            raise ValueError('negative values are not allowed')

        try:
            with _winreg.CreateKey(ScrConfig.HKCU, ScrConfig.PREFIX) as key:
                _winreg.SetValueEx(key, opt, 0, _winreg.REG_DWORD, value)

        except WindowsError as e:
            logging.warning(r'failed write to `HKCU\%s\%s`, value: %d, error: \
                    %s', ScrConfig.PREFIX, opt, value, e)

    def _get(self, opt):
        logging.debug('getting `%s`', opt)

        try:
            with _winreg.OpenKey(ScrConfig.HKCU, ScrConfig.PREFIX, 0,
                    _winreg.KEY_READ) as key:

                (value, _) = _winreg.QueryValueEx(key, opt)
                return value

        except WindowsError as e:
            logging.warning(r'failed read from `HKCU\%s\%s`, error: %s',
                    ScrConfig.PREFIX, opt, e)

    def _del(self, opt):
        logging.debug('deleting `%s`', opt)

        try:
            with _winreg.OpenKey(ScrConfig.HKCU, ScrConfig.PREFIX, 0,
                    _winreg.KEY_WRITE) as key:
                _winreg.DeleteValue(key, opt)

        except WindowsError as e:
            logging.warning(r'failed delete value from `HKCU\%s\%s`, error: %s',
                    ScrConfig.PREFIX, opt, e)

