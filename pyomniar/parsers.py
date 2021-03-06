
from pyomniar.utils import import_simplejson
from pyomniar.error import OmniarError

class Parser(object):

    def parse(self, method, payload):
        """
        Parse the response payload and return the result.
        Returns a tuple that contains the result data and the cursors
        (or None if not present).
        """
        raise NotImplementedError

    def parse_error(self, payload):
        """
        Parse the error message from payload.
        If unable to parse the message, throw an exception
        and default error message will be used.
        """
        raise NotImplementedError
        

class JSONParser(Parser):

    payload_format = 'json'

    def __init__(self):
        self.json_lib = import_simplejson()

    def parse(self, method, payload):
        try:
            json = self.json_lib.loads(payload)
        except Exception, e:
            raise OmniarError('Failed to parse JSON payload: %s' % e)

        return json

    def parse_error(self, payload):
        error = self.json_lib.loads(payload)
        if error.has_key('error-reason'):
            return error['error-reason']
        else:
            return error['error-code']
            

class EmptyParser(Parser):
    """Parser for items that don't return any data"""

    # def __init__(self):
    #     pass

    def parse(self, method, payload):
        return True

    def parse_error(self, payload):
        return False