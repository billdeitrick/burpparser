# Taken from https://stackoverflow.com/questions/2115410/does-python-have-a-module-for-parsing-http-requests-and-responses
from BaseHTTPServer import BaseHTTPRequestHandler
from httplib import HTTPResponse as BaseHTTPResponse
from StringIO import StringIO

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

class _FakeSocket():
    def __init__(self, response_str):
        self._file = StringIO(response_str)
    def makefile(self, *args, **kwargs):
        return self._file

class HTTPResponse(BaseHTTPResponse, object):
    def __init__(self, response_text):
        super(HTTPResponse, self).__init__(_FakeSocket(response_text))
        self.begin()
        self.content = self.read(len(response_text))