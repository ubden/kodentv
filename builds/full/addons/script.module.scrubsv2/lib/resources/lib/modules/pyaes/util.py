# Copyright (c) 2014 Richard Moore
# Why to_bufferable?
# Python 3 is very different from Python 2.x when it comes to strings of text
# and strings of bytes; in Python 3, strings of bytes do not exist, instead to
# represent arbitrary binary data, we must use the "bytes" object. This method
# ensures the object behaves as we need it to.

def to_bufferable(binary):
    return binary

def _get_byte(c):
    return ord(c)

try:
    xrange
except:
    def to_bufferable(binary):
        if isinstance(binary, bytes):
            return binary
        return bytes(ord(b) for b in binary)

    def _get_byte(c):
        return c

def append_PKCS7_padding(data):
    pad = 16 - (len(data) % 16)
    return data + to_bufferable(chr(pad) * pad)

def strip_PKCS7_padding(data):
    if len(data) % 16 != 0:
        raise ValueError("invalid length")
    pad = _get_byte(data[-1])
    if not pad or pad > 16:
        return data
    return data[:-pad]
