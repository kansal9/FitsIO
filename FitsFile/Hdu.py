#/usr/bin/env python3
# coding: utf-8

import os
import warnings

import numpy as np

from astropy.io import fits

from .File import *

__all__ = ['FitsHDU',]


class FitsHDU(FitsFile):
    def __init__(self, filename):
        super().__init__(filename)
        self.hdu_index = 0

    def set_hdu_index(self, index):
        self.hdu_index = index

    def get_hdu(self):
        return self.hdulist[self.hdu_index].header

    def list_keywords(self):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        return list(header.keys())

    def list_keyword_values(self, keywords):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        values = []
        for keyword in keywords:
            values.append(header[keyword])
        return values

    def keyword_exists(self, keyword):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        return keyword in header

    def write_keyword(self, keyword, value, comment=None):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        header[keyword] = (value, comment)
        self.hdulist.flush()

    def update_keyword(self, keyword, value, comment=None):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        header[keyword] = (value, comment)
        self.hdulist.flush()

    def delete_keyword(self, keyword):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        del header[keyword]
        self.hdulist.flush()

    def update_keyword_comment(self, keyword, comment):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        header.setcomment(keyword, comment)
        self.hdulist.flush()

    def write_history(self, history_entry):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        header.add_history(history_entry)
        self.hdulist.flush()

    def get_hduname(self):
        hdu = self.hdulist[self.hdu_index]
        return hdu.name

    def get_extname(self):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        return header.get("EXTNAME", default=None)

    def update_extname(self, extname):
        hdu = self.hdulist[self.hdu_index]
        header = hdu.header
        header["EXTNAME"] = extname
        self.hdulist.flush()

    def update_hduname(self, hduname):
        hdu = self.hdulist[self.hdu_index]
        hdu.name = hduname
        self.hdulist.flush()

    def fits_type(self):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.ImageHDU):
            print(f"HDU {hdu_index} of Fits file {self.filename} is IMAGE")
        elif isinstance(hdu, fits.BinTableHDU):
            print(f"HDU {hdu_index} of Fits file {self.filename} is BINTABLE")
        else:
            raise ValueError("HDU is not a binary table or an image")

    def add_primary_hdu(self, data=None, header=None):
        hdu = fits.PrimaryHDU(data=data, header=header)
        self.hdulist.append(hdu)

    def create_Image_hdu(self, data, header=None):
        hdu = fits.ImageHDU(data=data, header=header)
        self.hdulist.append(hdu)

    def create_bintable_hdu(self, data, header=None, name=None):
        cols = []
        for i, col_name in enumerate(data.dtype.names):
            col = fits.Column(name=col_name, format=data.dtype[i], array=data[col_name])
            cols.append(col)
        hdu = fits.BinTableHDU.from_columns(cols, header=header, name=name)
        self.hdulist.append(hdu)

    def delete_hdu(self):
        self.hdulist.pop(self.hdu_index)
        self.hdulist.flush()
