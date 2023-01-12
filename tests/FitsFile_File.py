#/usr/bin/env python3
# coding: utf-8

import unittest
import numpy as np
from FitsFile import File


class TestFitsFile(unittest.TestCase):

    def test_open_and_close(self):
        self.test_file = "/Users/kansal/Documents/GitHub/FitsIO/data/gal.fits"
        fits_file = File.FitsFile(self.test_file)
        fits_file.open()
        self.assertTrue(fits_file.hdulist is not None)
        fits_file.close()

    def test_file_exists(self):
        self.test_file = "/Users/kansal/Documents/GitHub/FitsIO/data/gal.fits"
        fits_file = File.FitsFile(self.test_file)
        self.assertTrue(fits_file.file_exists())
        

unittest.main()
