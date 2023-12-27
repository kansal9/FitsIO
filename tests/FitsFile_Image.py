#/usr/bin/env python3
# coding: utf-8

import unittest
from FitsFile import Image
import os

filepath = os.path.join(os.getcwd(), 'data', 'gal.fits')

class TestFitsFile(unittest.TestCase):

    def test_read_image_value_type(self):
        fits_file = Image.FitsImage(filepath)
        fits_file.open()
        self.assertEqual(fits_file.read_image_value_type(), 'float32')
        fits_file.close()

    def test_read_image_pixels(self):
        fits_file = Image.FitsImage(filepath)
        fits_file.open()
        self.assertEqual(fits_file.read_image_pixels(), 1936)
        fits_file.close()

    def test_get_shape(self):
        fits_file = Image.FitsImage(filepath)
        fits_file.open()
        self.assertEqual(fits_file.get_shape(), (44,44))
        fits_file.close()

    def test_redefine_size(self):
        fits_file = Image.FitsImage(filepath)
        fits_file.open()
        fits_file.redefine_size(0.5)
        self.assertEqual(fits_file.get_shape(), (22,22))
        fits_file.close()

unittest.main()
