# /usr/bin/env python3
# coding: utf-8

from astropy.io import fits
import numpy as np
from Hdu import *

__all__ = ['FitsBintable']


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
        hdu = self.hdulist[self.hdu_index]
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

    def add_column(self, name, formt, array):
        col = fits.Column(name=name, format=formt, array=array)
        self.hdulist[self.hdu_index].columns.add_col(col)

    def add_row(self, row):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            if len(row) == len(hdu.columns):
                new_row = np.array([tuple(row)], dtype=hdu.data.dtype)
                new_data = np.concatenate([hdu.data, new_row])
                new_hdu = fits.BinTableHDU(data=new_data, header=hdu.header)
                self.hdulist[self.hdu_index] = new_hdu
                self.hdulist.flush()
            else:
                raise ValueError("Number of values does not match the number of columns.")
        else:
            raise ValueError("HDU is not a binary table.")

    def add_rows(self, rows):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            if all(len(row) == len(hdu.columns) for row in rows):
                new_rows = np.array([tuple(row) for row in rows], dtype=hdu.data.dtype)
                new_data = np.concatenate([hdu.data, new_rows])
                new_hdu = fits.BinTableHDU(data=new_data, header=hdu.header)
                self.hdulist[self.hdu_index] = new_hdu
                self.hdulist.flush()
            else:
                raise ValueError("Number of columns in 'rows' does not match the number of columns in the table.")
        else:
            raise ValueError("HDU is not a binary table.")

    def delete_column(self, name):
        self.hdulist[self.hdu_index].columns.del_col(name)

    def delete_row(self, row_index):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            num_rows = hdu.data.shape[0]
            if 0 <= row_index < num_rows:
                new_data = np.delete(hdu.data, row_index, axis=0)
                new_hdu = fits.BinTableHDU(data=new_data, header=hdu.header)
                # Replace the existing HDU with the new one
                self.hdulist[self.hdu_index] = new_hdu
                self.hdulist.flush()
            else:
                raise ValueError(f"Row index {row_index} is out of bounds for the table.")
        else:
            raise ValueError("HDU is not a binary table.")

    def write_column_segment(self, name, data, start, stop):
        self.hdulist[self.hdu_index].data[name][start:stop] = data

    def read_column_segment(self, name, start, stop):
        return self.hdulist[self.hdu_index].data[name][start:stop]

    def sum_row(self, row_index):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            num_rows = hdu.data.shape[0]
            if 0 <= row_index < num_rows:
                return np.sum(hdu.data[row_index])
            else:
                raise ValueError(f"Row index {row_index} is out of bounds for the table.")
        else:
            raise ValueError("HDU is not a binary table.")

    def sum_col(self, column_name):
        hdu = self.hdulist[self.hdu_index]
        if isinstance(hdu, fits.BinTableHDU):
            columns = hdu.columns
            column_names = columns.names
            if column_name in column_names:
                return np.sum(hdu.data[column_name])
            else:
                raise ValueError(f"Column with name '{column_name}' not found in the table.")
        else:
            raise ValueError("HDU is not a binary table.")
