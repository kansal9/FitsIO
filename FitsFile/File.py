#/usr/bin/env python3
# coding: utf-8

import os
import warnings

import numpy as np
import logging

from astropy.io import fits
from astropy import units, wcs


__all__ = ['FitsFile',]


class FitsFile:
    def __init__(self, filename, readmode='readonly'): #readmode = ‘readonly’, ‘update’, ‘append’, ‘denywrite’, or ‘ostream’
        self.filename = filename
        self.mode = readmode

    def file_exists(self):
        return os.path.isfile(self.filename)

    def is_writable(self):
        return self.hdulist.writable()

    def is_open(self):
        return not self.hdulist.closed

    def open(self):
        if self.file_exists():
            self.hdulist = fits.open(self.filename, mode=self.mode)
        else:
            raise FileExistsError(f"Fits file {self.filename} doesn't exists....")

    def get_headers(self):
        headers = []
        for hdu in self.hdulist:
            headers.append(hdu.header)
        return headers

    def get_data(self, index):
        """Get the data from the specified HDU as a structured array."""
        return self.hdulist[index].data

    def get_num_headers(self):
        return len(self.hdulist)

    def save(self, new_filename=None, overwrite=False):
        if new_filename:
            self.hdulist.writeto(new_filename)
        elif (not overwrite) and file_exists():
            raise FileExistsError(f'File {self.filename} exists. Use `overwrite` to ignore')
        else:
            self.hdulist.writeto(self.filename, overwrite=overwrite)

    def close(self):
        if self.hdulist.fileinfo(0)['filemode'] in ('update', 'append'):
            self.hdulist.flush()
            self.hdulist.close(output_verify='ignore') #disable the verification of the data written to the FITS file (can be time-consuming)
        else:
            self.hdulist.close()

    def delete(self):
        self.close()
        os.remove(self.filename)
