import unittest
import random
from time import sleep
import os

from pyomniar import *

"""Configurations"""
# Must supply omniar account credentials for tests
api_key = ''
account_key = ''

class PyomniarAPITests(unittest.TestCase):
    def setUp(self):
        self.api = API(KeyAuthHandler(api_key=api_key, account_key=account_key))
        self.api.retry_count = 2
        self.api.retry_delay = 5
        
    def test_account_info(self):
        ret = self.api.get_account()
        print(ret)
    
    def test_get_scans(self):
        ret = self.api.get_scans()
        print(ret)
    
if __name__ == '__main__':

    unittest.main()