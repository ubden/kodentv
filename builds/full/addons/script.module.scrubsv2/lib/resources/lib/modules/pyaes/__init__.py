# Copyright (c) 2014 Richard Moore
# This is a pure-Python implementation of the AES algorithm and AES common
# modes of operation.
# See: https://en.wikipedia.org/wiki/Advanced_Encryption_Standard
# See: https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
# Supported key sizes:
#   128-bit
#   192-bit
#   256-bit
# Supported modes of operation:
#   ECB - Electronic Codebook
#   CBC - Cipher-Block Chaining
#   CFB - Cipher Feedback
#   OFB - Output Feedback
#   CTR - Counter
# See the README.md for API details and general information.
# Also useful, PyCrypto, a crypto library implemented in C with Python bindings:
# https://www.dlitz.net/software/pycrypto/

VERSION = [1, 3, 0]

from .aes import AES, AESModeOfOperationCTR, AESModeOfOperationCBC, AESModeOfOperationCFB, AESModeOfOperationECB, AESModeOfOperationOFB, AESModesOfOperation, Counter
from .blockfeeder import decrypt_stream, Decrypter, encrypt_stream, Encrypter
