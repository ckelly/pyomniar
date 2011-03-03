# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

"""
Pyomniar Omniar API library
"""
__version__ = '0.2.0'
__author__ = 'Chris Kelly'
__license__ = 'MIT'

from pyomniar.error import OmniarError
from pyomniar.api import API
from pyomniar.auth import KeyAuthHandler

def debug(enable=True, level=1):
    
    import httplib
    httplib.HTTPConnection.debuglevel = level