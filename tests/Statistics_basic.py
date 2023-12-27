# /usr/bin/env python3
# coding: utf-8

import unittest
from astropy.io import fits
import os
import numpy as np
from Statistics.basic_statistics import FitsStats

filepath = os.path.join(os.getcwd(), 'data', 'gal.fits')


class TestFitsStats(unittest.TestCase):
    def test_fits_image_stat(self):
        stats = FitsStats(filepath)
        fits_data = fits.getdata(filepath)
        fitsmin = np.min(fits_data)
        fitsmax = np.min(fits_data)
        fitsmean = np.min(fits_data)
        fitsstdev = np.min(fits_data)
        fitsmedian = np.min(fits_data)

        img_min, img_max, img_mean, img_stdev, img_median = stats.stats()

        self.assertEqual(img_min, fitsmin)
        self.assertEqual(img_max, fitsmax)
        self.assertEqual(img_mean, fitsmean)
        self.assertEqual(img_stdev, fitsstdev)
        self.assertEqual(img_median, fitsmedian)


unittest.main()
