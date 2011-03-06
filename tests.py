import unittest
import random
from time import sleep
import os

from pyomniar import *

"""Configurations"""
# Must supply omniar account credentials for tests
api_key = ''
account_key = ''

try:
    from test_settings import *
except ImportError:
    pass

class PyomniarAPITests(unittest.TestCase):
    def setUp(self):
        self.api = API(KeyAuthHandler(api_key=api_key, account_key=account_key))
        self.api.retry_count = 2
        self.api.retry_delay = 5
        
        self.scan_ids = []
        
    def test_account_info(self):
        '''Test call to get account info'''
        ret = self.api.get_account()
        print(ret)
    
    def test_get_scans(self):
        '''Test call to get Scans'''
        ret = self.api.get_scans()
        print(ret)
    
    def test_post_scans(self):
        ret = self.api.post_scans(os.getcwd()+'/test_data/atm_scan.zip', 
            name='tests_atm', 
            content='some ATM somewhere (this is a test upload)')
        ret_id = ret.get('scanUUID')
        if ret_id:
            self.scan_ids.append(ret_id)
        print(ret_id)
        print(ret)
        sleep(5)
        
    def tearDown(self):
        #for scan_id in self.scan_ids:
        #    ret = self.api.delete_scan(scan_id=scan_id)
        #    print(ret)

if __name__ == '__main__':
    unittest.main()