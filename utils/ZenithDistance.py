#/usr/bin/env python3
# coding: utf-8

import numpy as np
from astropy.coordinates import AltAz
from astropy.time import Time
import math

class ZenithDistance:
    def __init__(self, header):
        self.header = header
    """
    def get_zenith_distance(self):
        # Get the time and location information from the header
        time = Time(self.header['DATE-OBS'], format='isot')
        location = AltAz(location=self.header['LONG-OBS'], latitude=self.header['LAT-OBS'], height=self.header['ALT-OBS'])# ALT-OBS is in meters whereas Lat and lon in degrees?

        # Get the RA and DEC of the object from the header
        # In header, these valyes are in HH:MM:SS format
        # need to get tem in radians TODO
        ra = self.header['RA']
        dec = self.header['DEC']

        # Convert the RA and DEC to AltAz coordinates
        coords = AltAz(ra=ra, dec=dec, obstime=time, location=location)

        # Calculate the zenith distance
        zenith_distance = coords.zen.degree

        return zenith_distance
    """"
    def get_zenith_distance(self):
        airmass = self.header['AIRMASS']
        # Calculate the zenith distance using the airmass
        zenith_distance = math.acos(1/airmass)

        # Convert the zenith distance from radians to degrees
        zenith_distance = math.degrees(zenith_distance)

        return zenith_distance
