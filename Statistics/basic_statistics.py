# /usr/bin/env python3
# coding: utf-8

import numpy as np
from FitsFile.Hdu import *


class FitsStats(FitsHDU):
    """
        Calculate statistics for an image in a FITS file.

        Parameters:
            filename (str): The name of the FITS file.

        Returns:
            list: A list containing the calculated statistics [min, max, mean, stdev, median].
        """
    def __init__(self, filename):
        super().__init__(filename)
        # get image data
        self.img_data = self.hdulist[self.hdu_index].data
        self.header = self.hdulist[self.hdu_index].header

    def stats(self):
        # Calculate statistics using NumPy functions
        img_min = np.min(self.img_data)
        img_max = np.max(self.img_data)
        img_mean = np.mean(self.img_data)
        img_stdev = np.std(self.img_data)
        img_median = np.median(self.img_data)

        # print the results
        print(f"\nStats for {self.filename}:")
        print(f"\tRange = [{img_min}, {img_max}]")
        print(f"\tMean  = {img_mean:.6f} \t SD = {img_stdev:.6f}")
        print(f"\tMedian= {img_median:.6f}\n")

        # Return the stats
        return img_min, img_max, img_mean, img_stdev, img_median

    def centile(self, centile=None):
        """
        Provide the centile values of the image
        :param
            centile: specific centile value
        :return: [centval]: Returns the specified centile value
        """
        img_data = self.img_data.flatten()
        # Sort the flattened image data
        sorted_data = np.sort(img_data)

        # Calculate the median
        n = len(sorted_data)
        # idx1, idx2 = n // 2, n // 2 + 1
        # val1, val2 = sorted_data[idx1 - 1], sorted_data[idx2 - 1]
        # median = 0.5 * (val1 + val2) if n % 2 == 0 else sorted_data[(n - 1) // 2]

        # Get the minimum and maximum values
        img_min, img_max = sorted_data[0], sorted_data[-1]

        # Calculate centiles (percentiles)
        cent_list = [img_min] + [np.percentile(sorted_data, centile) for centile in range(1, 101)]

        # If Centile is provided, return the required centile value
        if centile is None:
            return cent_list
        else:
            cent = float(centile)
            if cent < 0.0:
                print(f"min={img_min}")
                return img_min
            if cent > 100.0:
                print(f"max={img_max}")
                return img_max
            idx = int(cent * n / 100) - 1
            print(f"Centile {cent} %\t {sorted_data[idx]:.6f}")
            return sorted_data[idx]

    def flux(self):
        dec_val = self.header['MEANDEC']
        ra_val = self.header['MEANRA']
