#/usr/bin/env python3
# coding: utf-8

import unittest
import numpy as np
from FitsFile import Bintable
import os

filepath = os.path.join(os.getcwd(), 'data', 'cat_shear.fits')

class TestFitsFile(unittest.TestCase):

    def test_get_num_rows(self):
        fits_file = Bintable.FitsBintable(filepath)
        fits_file.open()
        fits_file.set_hdu_index(1)
        self.assertEqual(fits_file.get_num_rows(), 190212)
        fits_file.close()

    def test_get_number_of_columns(self):
        fits_file = Bintable.FitsBintable(filepath)
        fits_file.open()
        fits_file.set_hdu_index(1)
        self.assertEqual(fits_file.get_number_of_columns(), 5)
        fits_file.close()

    def test_has_column(self):
        fits_file = Bintable.FitsBintable(filepath)
        fits_file.open()
        fits_file.set_hdu_index(1)
        self.assertTrue(fits_file.has_column('ra_gal'))
        fits_file.close()

    def test_find_column_index(self):
        fits_file = Bintable.FitsBintable(filepath)
        fits_file.open()
        fits_file.set_hdu_index(1)
        self.assertEqual(fits_file.find_column_index('shearE'), 2)
        fits_file.close()

    def test_update_column_name(self):
        fits_file = Bintable.FitsBintable(filepath)
        fits_file.open()
        fits_file.set_hdu_index(1)
        fits_file.update_column_name('ra_gal', 'ra')
        self.assertTrue(fits_file.has_column('ra'))
        fits_file.close()

unittest.main()
