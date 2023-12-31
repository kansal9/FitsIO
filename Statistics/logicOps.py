# /usr/bin/env python3
# coding: utf-8

import numpy as np
from FitsFile.Hdu import *
from astropy.io import fits
from astropy.convolution import convolve_fft, Box2DKernel


class FitsLogicOperations:
    def __init__(self, fitsfile1, fitsfile2=None):
        self.fitsfile1 = fitsfile1
        if fitsfile2 is not None:
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
    def stacked_image(filelist):
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
        average_array_first_list = self.stacked_image(filelist1)
        average_array_second_list = self.stacked_image(filelist2)

        # Subtract the average of the first list from the average of the second list
        result_array = average_array_second_list - average_array_first_list
        return result_array

    def contrast_stretching(self, min_out=None, max_out=None):
        """
        Apply contrast stretching.
        Parameters:
        - min_out: Minimum intensity value after stretching (default: None, uses the minimum in the input image)
        - max_out: Maximum intensity value after stretching (default: None, uses the maximum in the input image)

        Returns:
        - Stretched image
        """
        # Ensure the image is a numpy array
        image = np.array(fits.getdata(self.fitsfile1))
        # Calculate the minimum and maximum intensity values in the input image if not specified
        if min_out is None:
            min_out = np.min(image)
        if max_out is None:
            max_out = np.max(image)
        # Calculate the minimum and maximum intensity values in the input image
        min_in = np.min(image)
        max_in = np.max(image)
        # Apply contrast stretching using linear scaling
        stretched_image = ((image - min_in) / (max_in - min_in)) * (max_out - min_out) + min_out
        # Clip values to be within the specified output range
        stretched_image = np.clip(stretched_image, min_out, max_out)
        return stretched_image

    @staticmethod
    def perform_erosion(image, kernel_size=3):
        """
        Perform erosion operation on a given image.
        Parameters:
        - image: 2D numpy array representing the image
        - kernel_size: Size of the structuring element (default: 3)
        Returns:
        - Resulting image after erosion
        """
        kernel = Box2DKernel(width=kernel_size)
        return convolve_fft(image, kernel)

    @staticmethod
    def perform_dilation(image, kernel_size=3):
        """
        Perform dilation operation on a given image.
        Parameters:
        - image: 2D numpy array representing the image
        - kernel_size: Size of the structuring element (default: 3)
        Returns:
        - Resulting image after dilation
        """
        kernel = Box2DKernel(width=kernel_size)
        return convolve_fft(image, kernel, boundary='fill', fill_value=1)

    def perform_opening(self, kernel_size=3):
        """
        Perform opening operation on a given image.
        Parameters:
        - kernel_size: Size of the structuring element (default: 3)
        Returns:
        - Resulting image after opening
        """
        image = np.array(fits.getdata(self.fitsfile1))
        erosion_result = self.perform_erosion(image, kernel_size)
        return self.perform_dilation(erosion_result, kernel_size)

    def perform_closing(self, kernel_size=3):
        """
        Perform closing operation on a given image.
        Parameters:
        - kernel_size: Size of the structuring element (default: 3)
        Returns:
        - Resulting image after closing
        """
        image = np.array(fits.getdata(self.fitsfile1))
        dilation_result = self.perform_dilation(image, kernel_size)
        return self.perform_erosion(dilation_result, kernel_size)
