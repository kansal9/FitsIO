#/usr/bin/env python3
# coding: utf-8

import unittest
import numpy as np
from FitsFile import Hdu
import os

filepath = os.path.join(os.getcwd(), 'data', 'cat_shear.fits')

class TestFitsFile(unittest.TestCase):

    def test_keyword_exists(self):
        fits_file = Hdu.FitsHDU(filepath)
        fits_file.open()
        self.assertTrue(fits_file.keyword_exists('NAXIS'))
        fits_file.close()


unittest.main()
