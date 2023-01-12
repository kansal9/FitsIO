#/usr/bin/env python3
# coding: utf-8

import os
import warnings

import numpy as np

from astropy.io import fits

from .Hdu import *

__all__ = ['FitsImage',]


class FitsImage(FitsHDU):
    def __init__(self, filename):
        super().__init__(filename)

    def get_shape(self, hdu_index):
        return self.hdulist[hdu_index].data.shape

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

    def update_shape(self, new_shape):
        self.hdulist[self.hdu_index].data = self.hdulist[self.hdu_index].data.reshape(new_shape)

    def read_segment(self, start, stop):
        return self.hdulist[self.hdu_index].data[start[0]:stop[0], start[1]:stop[1]]


