# /usr/bin/env python3
# coding: utf-8

from skimage.transform import resize
import numpy as np
from Hdu import *

__all__ = ['FitsImage']


class FitsImage(FitsHDU):
    def __init__(self, filename):
        super().__init__(filename)

    def get_shape(self):
        return self.hdulist[self.hdu_index].data.shape

    def read_image_value_type(self):
        hdu = self.hdulist[0]
        if hdu.data is not None:
            return hdu.data.dtype.name
        else:
            return None

    def update_type(self, new_dtype):
        self.hdulist[self.hdu_index].data = self.hdulist[self.hdu_index].data.astype(new_dtype)

    def read_image_pixels(self):
        return self.hdulist[self.hdu_index].data.size

    def scale_image(self, factor):
        return self.hdulist[self.hdu_index].data * factor

    def shift_image(self, factor):
        return self.hdulist[self.hdu_index].data + factor

    def dump_row(self, row_no, axis=0):
        # Dumps the pixel values of a specified row of the image
        new_data = np.delete(self.hdulist[self.hdu_index].data, row_no, axis=axis)
        return new_data

    def transpose(self):
        new_data = np.transpose(self.hdulist[self.hdu_index].data)
        return new_data

    def sum_row(self, row_idx, data_range=None):
        data = self.hdulist[self.hdu_index].data
        if data_range is None:
            # summing the entire row
            val = data[row_idx, :].sum()
        else:
            # summing within a specified range
            start, end = data_range
            val = data[row_idx, start:end + 1].sum()
        return val

    def sum_col(self, col_idx):
        val = self.hdulist[self.hdu_index].data[:, col_idx].sum()
        return val

    def redefine_size(self, scaling_factor):
        new_shape = tuple(map(lambda x: int(x * scaling_factor), self.hdulist[0].data.shape))
        new_data = resize(self.hdulist[0].data, new_shape)
        self.hdulist[0].data = new_data
        # Update the size of the image in the header
        self.hdulist[self.hdu_index].header['NAXIS1'] = new_shape[1]
        self.hdulist[self.hdu_index].header['NAXIS2'] = new_shape[0]
        self.hdulist.flush()

    def read_segment(self, start, stop):
        return self.hdulist[self.hdu_index].data[start[0]:stop[0], start[1]:stop[1]]
