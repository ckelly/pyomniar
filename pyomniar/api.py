# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

import os

from pyomniar.binder import bind_api
from pyomniar.parsers import JSONParser, EmptyParser
from pyomniar.utils import import_simplejson, encode_multipart_formdata, build_postdata_tup, build_file_tup
json = import_simplejson()


class API(object):
    '''Omniar API'''
    
    def __init__(self, auth_handler,
            host='api.omniar.com', api_root='/v1b', secure=False,
            retry_count=0, retry_errors=None, retry_delay=0, parser=None):
            # short circuit this for now, change if we need Oauth, etc later
        self.auth = auth_handler
        self.host = host
        self.api_root = api_root
        self.secure = secure
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.parser = parser or JSONParser()
        
    # Pyomniar method calls
    get_account = bind_api(
        path = '/accounts/{account_key}',
        allowed_param = []
    )
    
    # get_scans
    get_scans = bind_api(
        path = '/accounts/{account_key}/scans',
        allowed_param = []
    )
    
    # get single scan
    get_scan = bind_api(
        path = '/accounts/{account_key}/scans/{scan_id}',
        allowed_param = ['scan_id']
    )
    
    # post scans
    def post_scans(self, filename, name=None, content=None):
        meta = {}
        if name:
            meta['name'] = name
        if content:
            meta['content'] = content
        form_meta = build_postdata_tup(json.dumps(meta), 'json')
        
        files = build_file_tup(filename, 'scanFile')
        
        headers, post_data = encode_multipart_formdata(form_meta, files)
        return bind_api(
            path = '/accounts/{account_key}/scans',
            method = 'POST',
        )(self, post_data=post_data, headers=headers)

    # update scan
    def update_scan(self, scan_id, name=None, content=None):
        meta = {}
        if name:
            meta['name'] = name
        if content:
            meta['content'] = content

        post_data = json.dumps(meta)
        return bind_api(
            path = '/accounts/{account_key}/scans/{scan_id}',
            method = 'PUT',
            allowed_param = ['scan_id']
        )(self, scan_id=scan_id, post_data=post_data)

    
    def delete_scan(self, scan_id):
        return bind_api(
            path = '/accounts/{account_key}/scans/{scan_id}',
            method = 'DELETE',
            allowed_param = ['scan_id']
        )(self, scan_id=scan_id, parser=EmptyParser())


    def match(self, filename):
        files = build_file_tup(filename, 'file')
        headers, post_data = encode_multipart_formdata([], files)
        
        return bind_api(
            path = '/accounts/{account_key}/match',
            method = 'POST',
        )(self, post_data=post_data, headers=headers)

