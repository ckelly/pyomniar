# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

import urllib
from urllib2 import Request, urlopen

from pyomniar.error import OmniarError

class AuthHandler(object):

    def apply_auth(self, url, method, headers, parameters):
        """Apply authentication headers to request"""
        raise NotImplementedError
    
    def append_auth(self, url, method, headers, parameters):
        """Apply certain authentication to url as params"""
        raise NotImplementedError
    
    def get_account_key(self):
        """Return the account_key of the authenticated user"""
        raise NotImplementedError

class KeyAuthHandler(AuthHandler):
    
    def __init__(self, api_key, account_key):
        self.api_key = api_key
        self.account_key = account_key
    
    # def apply_auth(self, url, method, headers, parameters):
    #     key = urllib.urlencode({'apikey': self.api_key})
    #     if not len(parameters):
    #         url += '?'
    #     else:
    #         url += "&"
    #     url += key
        
    def append_auth(self, url, method, headers, parameters):
        parameters['apikey'] = self.api_key
        
    def apply_auth(self, url, method, headers, parameters):
        pass
        
    def get_account_key(self):
        return self.account_key