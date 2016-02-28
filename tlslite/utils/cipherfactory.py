# Author: Trevor Perrin
#
# Efthimios Iosifidis - Speck Cipher 
# See the LICENSE file for legal information regarding use of this file.

"""Factory functions for symmetric cryptography."""

import os

from tlslite.utils import python_aes
from tlslite.utils import python_aesgcm
from tlslite.utils import python_chacha20_poly1305
from tlslite.utils import python_rc4
from tlslite.utils import python_speck
from tlslite.utils import python_speck128gcm
from tlslite.utils import python_speck192gcm

from tlslite.utils import cryptomath

tripleDESPresent = False

if cryptomath.m2cryptoLoaded:
    from tlslite.utils import openssl_aes
    from tlslite.utils import openssl_rc4
    from tlslite.utils import openssl_tripledes
    tripleDESPresent = True

if cryptomath.pycryptoLoaded:
    from tlslite.utils import pycrypto_aes
    from tlslite.utils import pycrypto_aesgcm
    from tlslite.utils import pycrypto_rc4
    from tlslite.utils import pycrypto_tripledes
    tripleDESPresent = True

# **************************************************************************
# Factory Functions for AES
# **************************************************************************

def createAES(key, IV, implList=None):
    """Create a new AES object.

    @type key: str
    @param key: A 16, 24, or 32 byte string.

    @type IV: str
    @param IV: A 16 byte string

    @rtype: L{tlslite.utils.AES}
    @return: An AES object.
    """
    if implList is None:
        implList = ["openssl", "python", "pycrypto" ]

    for impl in implList:
        if impl == "openssl" and cryptomath.m2cryptoLoaded:
            return openssl_aes.new(key, 2, IV)
        elif impl == "pycrypto" and cryptomath.pycryptoLoaded:
            return pycrypto_aes.new(key, 2, IV)
        elif impl == "python":
            return python_aes.new(key, 2, IV)
    raise NotImplementedError()

def createSPECK(key, IV, implList=None):
    """Create a new SPECK object.

    @type key: str
    @param key: A 16 byte string.

    @type IV: str
    @param IV: A 16 byte string

    @rtype: L{tlslite.utils.SPECK}
    @return: A SPECK object.
    """
    if implList is None:
        implList = ["python"]

    for impl in implList:
        if impl == "python":
            return python_speck.new(key,IV)
    raise NotImplementedError()

def createAESGCM(key, implList=None):
    """Create a new AESGCM object.

    @type key: bytearray
    @param key: A 16 or 32 byte byte array.

    @rtype: L{tlslite.utils.AESGCM}
    @return: An AESGCM object.
    """
    if implList is None:
        implList = ["pycrypto", "python"]

    for impl in implList:
        if impl == "pycrypto" and cryptomath.pycryptoLoaded:
            return pycrypto_aesgcm.new(key)
        if impl == "python":
            return python_aesgcm.new(key)
    raise NotImplementedError()


def createSPECK128GCM(key, implList=None):
    """Create a new SPECKGCM object.

    @type key: bytearray
    @param key: A 16 or 32 byte byte array.

    @rtype: L{tlslite.utils.AESGCM}
    @return: An AESGCM object.
    """
    if implList is None:
        implList = ["python"]

    for impl in implList:
        if impl == "python":
            return python_speck128gcm.new(key)
    raise NotImplementedError()


def createSPECK192GCM(key, implList=None):
    """Create a new SPECKGCM object.

    @type key: bytearray
    @param key: A 16 or 32 byte byte array.

    @rtype: L{tlslite.utils.AESGCM}
    @return: An AESGCM object.
    """
    if implList is None:
        implList = ["python"]

    for impl in implList:
        if impl == "python":
            return python_speck192gcm.new(key)
    raise NotImplementedError()



def createCHACHA20(key, implList=None):
    """Create a new CHACHA20_POLY1305 object.

    @type key: bytearray
    @param key: a 32 byte array to serve as key

    @rtype: L{tlslite.utils.CHACHA20_POLY1305}
    @return: A ChaCha20/Poly1305 object
    """
    if implList is None:
        implList = ["python"]

    for impl in implList:
        if impl == "python":
            return python_chacha20_poly1305.new(key)
    raise NotImplementedError()

def createRC4(key, IV, implList=None):
    """Create a new RC4 object.

    @type key: str
    @param key: A 16 to 32 byte string.

    @type IV: object
    @param IV: Ignored, whatever it is.

    @rtype: L{tlslite.utils.RC4}
    @return: An RC4 object.
    """
    if implList is None:
        implList = ["openssl", "pycrypto", "python"]

    if len(IV) != 0:
        raise AssertionError()
    for impl in implList:
        if impl == "openssl" and cryptomath.m2cryptoLoaded:
            return openssl_rc4.new(key)
        elif impl == "pycrypto" and cryptomath.pycryptoLoaded:
            return pycrypto_rc4.new(key)
        elif impl == "python":
            return python_rc4.new(key)
    raise NotImplementedError()

#Create a new TripleDES instance
def createTripleDES(key, IV, implList=None):
    """Create a new 3DES object.

    @type key: str
    @param key: A 24 byte string.

    @type IV: str
    @param IV: An 8 byte string

    @rtype: L{tlslite.utils.TripleDES}
    @return: A 3DES object.
    """
    if implList is None:
        implList = ["openssl", "pycrypto"]

    for impl in implList:
        if impl == "openssl" and cryptomath.m2cryptoLoaded:
            return openssl_tripledes.new(key, 2, IV)
        elif impl == "pycrypto" and cryptomath.pycryptoLoaded:
            return pycrypto_tripledes.new(key, 2, IV)
    raise NotImplementedError()
