# /usr/bin/env python3
# coding: utf-8

import numpy as np
from FitsFile.Hdu import *
from astropy.io import fits


class FitsLogicOperations:
    def __init__(self, fitsfile1, fitsfile2):
        self.fitsfile1 = fitsfile1
        self.fitsfile2 = fitsfile2

    def perform_and_operation(self):
        with fits.open(self.fitsfile1, mode='readonly') as f1, fits.open(self.fitsfile2, mode='readonly') as f2:
            # img1_dim = f1[0].data.shape

            img1 = f1[0].data.astype(np.int32)
            img2 = f2[0].data.astype(np.int32)

            outimg = np.logical_and(img1, img2).astype(np.int32)

            return outimg

    def perform_subtraction(self):
        with fits.open(self.fitsfile1, mode='readonly') as f1, fits.open(self.fitsfile2, mode='readonly') as f2:
            imgdim1 = f1[0].data.shape
            imgdim2 = f2[0].data.shape
            if imgdim1 != imgdim2:
                raise ValueError(f"Images {self.fitsfile1} and {self.fitsfile2} are incompatible")

            img1 = f1[0].data
            img2 = f2[0].data

            return img1-img2

    @staticmethod
    def get_average_image(filelist):
        first_fits_file = fits.open(filelist[0])
        data_shape = first_fits_file[0].data.shape
        # Initialize an array to store the sum of pixel values
        sum_array = np.zeros(data_shape, dtype=np.float64)
        first_fits_file.close()

        # Loop through all FITS files and accumulate pixel values
        for fits_file in filelist:
            hdul = fits.open(fits_file)
            sum_array += hdul[0].data
            hdul.close()

        # Calculate the average by dividing the sum by the number of files
        new_img = sum_array / len(filelist)

        return new_img

    def fowler(self, filelist1, filelist2):
        # Create a new image based on the subtraction of the average of the first list from the
        # average of the second list.
        average_array_first_list = self.get_average_image(filelist1)
        average_array_second_list = self.get_average_image(filelist2)

        # Subtract the average of the first list from the average of the second list
        result_array = average_array_second_list - average_array_first_list
        return result_array
