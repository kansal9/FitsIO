# /usr/bin/env python3
# coding: utf-8

import numpy as np
from FitsFile.Hdu import *
from astropy.convolution import convolve, Gaussian2DKernel
from scipy.stats import skew, kurtosis


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

    def smoothing(self, kernel_size=3, smoothing=True):
        """
        Apply image smoothing or sharpening using convolution to a FITS image.
        Parameters:
        - kernel_size: Size of the convolution kernel (default: 3)
        - smoothing: If True, apply smoothing; if False, apply sharpening (default: True)
        Returns:
        - Processed image
        """
        # Ensure the image is a numpy array
        image = np.array(self.img_data)
        # Define the convolution kernel for smoothing or sharpening
        if smoothing:
            sigma = kernel_size / 2
            kernel = Gaussian2DKernel(x_stddev=sigma, y_stddev=sigma)
        else:
            kernel = np.array([[-1, -1, -1],
                               [-1, 9, -1],
                               [-1, -1, -1]], dtype=np.float32)

        # Apply convolution to the image
        processed_image = convolve(image, kernel, boundary='extend')
        # Clip values to be within the valid intensity range
        processed_image = np.clip(processed_image, 0, 65535)  # Assuming 16-bit FITS image
        return processed_image

    def skewness(self):
        """
        Calculate skewness of pixel values in a given image.
        Parameters:
        - image: 2D numpy array representing the image
        Returns:
        - Skewness value
        """
        flattened_image = self.img_data.flatten()
        return skew(flattened_image)

    def calculate_kurtosis(self):
        """
        Calculate kurtosis of pixel values in a given image.
        Parameters:
        - image: 2D numpy array representing the image
        Returns:
        - Kurtosis value
        """
        flattened_image = self.img_data.flatten()
        return kurtosis(flattened_image)

    def radial_profile(self, center=None):
        """
            Calculate the radial profile of a 2D image.
            Parameters:
            - center (tuple): Coordinates (x, y) of the center around which to calculate the radial profile.
              center = (image_size // 2, image_size // 2)
            Returns:
            - ndarray: Radial profile, representing the average intensity at each radial distance from the center.
            """
        y, x = np.indices(self.img_data.shape)
        if center is None:
            height = self.header['NAXIS1']
            width = self.header['NAXIS2']
            center = (width // 2, height // 2)
        r = np.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
        r = r.astype(int)
        tbin = np.bincount(r.ravel(), self.img_data.ravel())
        nr = np.bincount(r.ravel())
        rprofile = tbin / nr
        return rprofile

    def flux(self):
        # ToDo: input reduced 2dfdr data file.. How?
        dec_val = self.header['MEANDEC']
        ra_val = self.header['MEANRA']
