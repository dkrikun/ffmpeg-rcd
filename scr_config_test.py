# coding: utf-8

import unittest
import subprocess

from scr_config import *

class ScrConfigTest(unittest.TestCase):

    def test_getx_empty(self):

        # remove from registry
        subprocess.call(r'reg delete HKCU\Software\screen-capture-recorder \
                /v start_x /f')

        self.assertIsNone(ScrConfig().x)

    def test_getx(self):
        x = 1024

        # add to registry
        subprocess.call(r'reg add HKCU\Software\screen-capture-recorder \
                /v start_x /t REG_DWORD /d {0} /f'.format(hex(x)))

        self.assertEqual(ScrConfig().x, x)

    def test_setx(self):
        x = 1024
        ScrConfig().x = x

        try:
            stdio = subprocess.check_output(r'reg query \
                    HKCU\Software\screen-capture-recorder \
                    /v start_x /t REG_DWORD')
        except subprocess.CalledProcessError:
            self.fail('req query failed')

        # reg query output is expected to contain the value of x in hex
        self.assertRegexpMatches(stdio, hex(x))

    def test_delx(self):
        # add `start_x` value to registry
        subprocess.call(r'reg add HKCU\Software\screen-capture-recorder \
                /v start_x /t REG_DWORD /d 0 /f')

        del ScrConfig().x
        rc = subprocess.call(r'reg query HKCU\Software\screen-capture-recorder \
                /v start_x /t REG_DWORD')

        # req query is expected to fail now
        self.assertNotEqual(rc, 0)

    # test aero separately because it's boolean
    def test_aero(self):
        ScrConfig().disable_aero = True

        try:
            stdio = subprocess.check_output(r'reg query \
                    HKCU\Software\screen-capture-recorder \
                    /v disable_aero_for_vista_plus_if_1 \
                    /t REG_DWORD')
        except subprocess.CalledProcessError:
            self.fail('req query failed')

        self.assertRegexpMatches(stdio, '0x1')

if __name__ == '__main__':
    unittest.main()


