# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

import mimetypes

def convert_to_utf8_str(arg):
    # written by Michael Norton (http://docondev.blogspot.com/)
    if isinstance(arg, unicode):
        arg = arg.encode('utf-8')
    elif not isinstance(arg, str):
        arg = str(arg)
    return arg

def import_simplejson():
    try:
        import json  # Python 2.6+
    except ImportError:
        try:
            import simplejson as json
        except ImportError:
            try:
                from django.utils import simplejson as json  # Google App Engine
            except ImportError:
                raise ImportError, "Can't load a json library"

    return json

def build_file_tup(filename, field_name):
    fp = open(filename, 'rb')
    return [(field_name, filename, fp.read())]

def build_image_tup(filename, field_name):
    file_type = get_content_type(filename)
    if file_type not in ['image/jpeg']:
        raise OmniarError('Invalid file type for image: %s. Only jpg images are currently allowed' % file_type)
    
    return build_file_tup(filename, field_name)

def build_postdata_tup(data, field_name):
    return [(field_name, data)]

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (headers, body) ready for httplib.HTTP instance
    
    based on http://code.activestate.com/recipes/146306/
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(convert_to_utf8_str(value))
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    
    # build headers
    headers = {
        'Content-Type': 'multipart/form-data; boundary=%s' % BOUNDARY,
        'Content-Length': len(body)
    }
    
    return headers, body

def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
