import unittest
import random
from time import sleep
import os

from pyomniar import *

class OmniarTestError(Exception):
    """Omniar test exception"""

    def __init__(self, reason):
        self.reason = unicode(reason)

    def __str__(self):
        return self.reason


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
        self.updated_content = "updated_name_content"
    
    def _wait_for_ready(self, scan_id):
        print('waiting for scan to process')
        loopout = 60 #(10 mins)
        count = 0
        while count < loopout:
            single = self.api.get_scan(scan_id=scan_id)
            if single['status'] == 'scan_building':
                sleep(10)
            else:
                break
            count += 1

        if single['status'] != 'scan_active':
            raise OmniarTestError('Scan did not process')
    
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
        
        # get single scan by id
        print("get single scan")
        single = self.api.get_scan(scan_id=ret_id)
        single_id = ret.get('scanUUID')
        self.assertEqual(ret_id, single_id)
        
        self._wait_for_ready(ret_id)
        
        # update scan with new data
        print("update scan")
        update = self.api.update_scan(ret_id,
            name = self.updated_name,
            content = self.updated_content
        )
        
        sleep(10)
        
        print("get updated scan")
        # get updated scan by id
        updated = self.api.get_scan(scan_id=ret_id)
        updated_name = updated.get('name')
        updated_content = updated.get('content')
        self.assertEqual(updated_name, self.updated_name)
        self.assertEqual(updated_content, self.updated_content)

    # def test_post_match(self):
    #         ret = self.api.post_scans(os.getcwd()+'/test_data/atm_scan.zip', 
    #             name='tests_atm_match', 
    #             content='atm scans (this is a test upload for matching)')
    #         ret_id = ret.get('scanUUID')
    #         print ret_id
    #         if ret_id:
    #             self.scan_ids.append(ret_id)
    #     
    #         # get single scan by id
    #         print("waiting for scan to build (this may take a while)")
    #         # wait for scan to build
    #         self._wait_for_ready(ret_id)
    #     
    #         # do match
    #         match = self.api.match(os.getcwd()+'/test_data/atm_scan_match.jpg')
    #         # match should be a list
    #         print("MATCH RETURNED")
    #         print(match)
    #         self.assertTrue(match)
    #         
    #         match_id = match[0]['scanUUID']
    #         self.assertEqual(ret_id, match_id)
    
    def tearDown(self):
        for scan_id in self.scan_ids:
            scan = self.api.get_scan(scan_id=scan_id)
            if scan['status'] == 'scan_active':
                ret = self.api.delete_scan(scan_id=scan_id)
                print('scan %s deleted' % (scan_id))
            else:
                print("scan %s skipped, not ready" % (scan_id))

if __name__ == '__main__':
    unittest.main()