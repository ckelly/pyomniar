# Pyomniar
# Copyright 2011 Chris Kelly
# See LICENSE for details.

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