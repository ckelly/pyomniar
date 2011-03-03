# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

import os
import mimetypes

from pyomniar.binder import bind_api
from pyomniar.parsers import JSONParser
from pyomniar.utils import import_simplejson
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
    
    # post_scans
    
    get_scans = bind_api(
        path = '/accounts/{account_key}/scans',
        allowed_param = []
    )
    
    get_single_scan = bind_api(
        path = '/accounts/{account_key}/scans/{scan_uuid}',
        allowed_param = ['scan_uuid']
    )
    
    update_scan = bind_api(
        path = '/accounts/{account_key}/scans/{scan_uuid}',
        method = 'PUT',
        allowed_param = ['scan_uuid']
    )
    
    """ Internal use only """
    @staticmethod
    def _pack_file(filename, max_size):
        """Pack image from file into multipart-formdata post body"""
        # image must be less than 700kb in size
        try:
            if os.path.getsize(filename) > (max_size * 1024):
                raise OmniarError('File is too big, must be less than 700kb.')
        except os.error, e:
            raise OmniarError('Unable to access file')

        # image must be gif, jpeg, or png
        file_type = mimetypes.guess_type(filename)
        if file_type is None:
            raise OmniarError('Could not determine file type')
        file_type = file_type[0]
        if file_type not in ['image/gif', 'image/jpeg', 'image/png']:
            raise OmniarError('Invalid file type for image: %s' % file_type)

        # build the mulitpart-formdata body
        fp = open(filename, 'rb')
        BOUNDARY = 'Tw3ePy'
        body = []
        body.append('--' + BOUNDARY)
        body.append('Content-Disposition: form-data; name="image"; filename="%s"' % filename)
        body.append('Content-Type: %s' % file_type)
        body.append('')
        body.append(fp.read())
        body.append('--' + BOUNDARY + '--')
        body.append('')
        fp.close()
        body = '\r\n'.join(body)

        # build headers
        headers = {
            'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
            'Content-Length': len(body)
        }

        return headers, body
    
    