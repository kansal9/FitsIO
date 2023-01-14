#/usr/bin/env python3
# coding: utf-8

import unittest
import numpy as np
from FitsFile import File
import os

filepath = os.path.join(os.getcwd(), 'data', 'gal.fits')

class TestFitsFile(unittest.TestCase):

    def test_open_and_close(self):
        self.test_file = filepath
        fits_file = File.FitsFile(self.test_file)
        fits_file.open()
        self.assertTrue(fits_file.hdulist is not None)
        fits_file.close()

    def test_file_exists(self):
        fits_file = File.FitsFile(filepath)
        self.assertTrue(fits_file.file_exists())

    def test_get_num_headers(self):
        fits_file = File.FitsFile(filepath)
        fits_file.open()
        self.assertEqual(fits_file.get_num_headers(), 1)
        fits_file.close()

unittest.main()
