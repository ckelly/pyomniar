# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

class OmniarError(Exception):
    """Omniar exception"""

    def __init__(self, reason, response=None):
        self.reason = unicode(reason)
        self.response = response

    def __str__(self):
        return self.reason