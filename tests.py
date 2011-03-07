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
        
        self.updated_name = "updated_name_atm"
        self.updated_desc = "updated_name_content"
        
    def test_account_info(self):
        '''Test call to get account info'''
        ret = self.api.get_account()
        print(ret)
    
    def test_get_scans(self):
        '''Test call to get Scans'''
        ret = self.api.get_scans()
        for r in ret:
            self.api.delete_scan(r['scanUUID'])
        print(ret)
    
    def test_post_get_update(self):
        ret = self.api.post_scans(os.getcwd()+'/test_data/atm_scan.zip', 
            name='tests_atm', 
            content='some ATM somewhere (this is a test upload)')
        ret_id = ret.get('scanUUID')
        if ret_id:
            self.scan_ids.append(ret_id)
        print(ret_id)
        print(ret)
        sleep(5)
        
        # get single scan by id
        print("get single scan")
        single = self.api.get_scan(scan_id=ret_id)
        single_id = ret.get('scanUUID')
        self.assertEqual(ret_id, single_id)
        
        # # update scan with new data
        #         print("update scan")
        #         update = self.api.update_scan(ret_id,
        #             name=self.updated_name
        #             #content=self.updated_desc
        #         )
        #         sleep(5)
        #         
        #         print("get updated scan")
        #         # get updated scan by id
        #         updated = self.api.get_scan(scan_id=ret_id)
        #         updated_name = ret.get('name')
        #         updated_content = ret.get('content')
        #         self.assertEqual(updated_name, self.updated_name)
        #         #self.assertEqual(updated_content, self.updated_content)
        
        
    def tearDown(self):
        for scan_id in self.scan_ids:
            ret = self.api.delete_scan(scan_id=scan_id)
            print(ret)

if __name__ == '__main__':
    unittest.main()