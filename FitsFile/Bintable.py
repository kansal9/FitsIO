#/usr/bin/env python3
# coding: utf-8

import os
import numpy as np

from astropy.io import fits

from .Hdu import *

__all__ = ['FitsBintable',]


class FitsBintable(FitsHDU):
    def __init__(self, filename):
        super().__init__(filename)

    def get_column_names(self):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            columns = hdu.columns
            column_names = columns.names
            return column_names
        else:
            raise ValueError("HDU is not a binary table.")

    def get_column_data(self, column_name):
        """Get a column from the specified HDU as a numpy array."""
        hdu = self.hdulist[self.hdu_index ]
        if isinstance(hdu, fits.BinTableHDU):
            return hdu.data[column_name]
        else:
            raise ValueError("HDU is not a binary table")

    def get_num_rows(self):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            return hdu.data.shape[0]
        else:
            raise ValueError("HDU is not a binary table")

    def get_number_of_columns(self):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            return len(hdu.columns)
        else:
            raise ValueError("HDU is not a binary table.")

    def has_column(self, column_name):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            columns = hdu.columns
            column_names = columns.names
            return column_name in column_names
        else:
            raise ValueError("HDU is not a binary table.")

    def update_column_name(self, column_name, new_name):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            columns = hdu.columns
            if column_name in columns.names:
                columns[column_name].name = new_name
                self.hdulist.flush()
            else:
                raise ValueError(f"Column with name '{column_name}' not found in HDU.")
        else:
            raise ValueError("HDU is not a binary table.")

    def find_column_index(self, column_name):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            columns = hdu.columns
            column_names = columns.names
            if column_name in column_names:
                return column_names.index(column_name)
            else:
                raise ValueError(f"Column with name '{column_name}' not found in HDU.")
        else:
            raise ValueError("HDU is not a binary table.")

    def add_column(self, name, format, array):
        col = fits.Column(name=name, format=format, array=array)
        self.hdulist[self.hdu_index].columns.add_col(col)

    def delete_column(self, name):
        self.hdulist[self.hdu_index].columns.del_col(name)

    def write_column_segment(self, name, data, start, stop):
        self.hdulist[self.hdu_index].data[name][start:stop] = data

    def read_column_segment(self, name, start, stop):
        return self.hdulist[self.hdu_index].data[name][start:stop]
