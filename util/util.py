"""
@Author: Rossi
2016-01-24
"""
import urllib
import base64
import time

OK = 200


def quote_base64_encode(text):
    """
    Quoting and encoding string using base64 encoding.
    """
    quote_text = urllib.quote(text)
    quote_text = base64.b64encode(bytearray(quote_text, 'utf-8'))
    return urllib.quote(quote_text)


def base64_encode(text):
    return str(base64.b64encode(bytearray(text, 'utf-8')), 'utf-8')


def get_systemtime():
    """
    Getting system time
    """
    t = str(time.time())
    t = t.replace(".", "")[:-3]
    return t


def check_status(r):
    return r.status_code == OK
