# Author: Google
# Reuse of code by Efthimios Iosifidis for SPECK192GCM
#
# """Pure-Python SPECK-GCM implementation."""
#
#
# See the LICENSE file for legal information regarding use of this file.

# GCM works over elements of the field GF(2^128), each of which is a 128-bit
# polynomial. Throughout this implementation, polynomials are represented as
# Python integers with the low-order terms at the most significant bits. So a
# 128-bit polynomial is an integer from 0 to 2^128-1 with the most significant
# bit representing the x^0 term and the least significant bit representing the
# x^127 term. This bit reversal also applies to polynomials used as indices in a
# look-up table.

from __future__ import division
from .cryptomath import bytesToNumber, numberToByteArray
import time 


def new(key):
    return SPECK192GCM(key)


class SPECK192GCM(object):
    """
    SPECK-GCM implementation. Note: this implementation does not attempt
    to be side-channel resistant. It's also rather slow.
    """

    def __init__(self, key):
        self.isBlockCipher = False
        self.isAEAD = True
        self.nonceLength = 12
        self.tagLength = 16
        self.implementation = "python"
        
        if len(key) == 24:
            self.name = "speck192gcm"
            self.key = key
            
            #convert the key bytesarray to int
            self.key = bytesToNumber(key)            
        else:
            raise AssertionError()
        
        self.block_size = 16
        self.rounds = 33
        self.word_size = 64         # alpha_shift = 8 , beta_shift = 3        
        
        
        # Create Properly Sized bit mask for truncating addition and left shift outputs          
        self.mod_mask = (2 ** 64) - 1 
        
        
        
        # Parse the given key and truncate it to the key length
        try:
            self.key = self.key & ((2 ** 192) - 1)
        except (ValueError, TypeError):
            print('Invalid Key Value!')
            print('Please Provide Key as int')
            raise
        
        # Pre-compile key schedule
        self.key_schedule = [self.key & self.mod_mask]
        l_schedule = [(self.key >> (x * self.word_size)) & self.mod_mask for x in xrange(1, 192 // self.word_size)]
        
        key_schedule = self.key_schedule
        
        for x in xrange(32):  #rounds - 1
            new_l_k = self.encrypt_round(l_schedule[x], key_schedule[x], x)
            l_schedule.append(new_l_k[0])
            key_schedule.append(new_l_k[1])


        encrypt = self.encrypt
        # The GCM key is SPECK(0).
        h = bytesToNumber(encrypt(bytearray(16)))

        # Pre-compute all 4-bit multiples of h. Note that bits are reversed
        # because our polynomial representation places low-order terms at the
        # most significant bit. Thus x^0 * h = h is at index 0b1000 = 8 and
        # x^1 * h is at index 0b0100 = 4.
        self._productTable = [0] * 16
        self._productTable[self._reverseBits(1)] = h
        for i in xrange(2, 16, 2):
            self._productTable[self._reverseBits(i)] = \
                self._gcmShift(self._productTable[self._reverseBits(i//2)])
            self._productTable[self._reverseBits(i+1)] = \
                self._gcmAdd(self._productTable[self._reverseBits(i)], h)

    def _rawSpeckCtrEncrypt(self, counter, inp):
        """
        Encrypts (or decrypts) plaintext with SPECK-CTR. counter is modified.
        """
        out = bytearray(len(inp))
        
        encrypt = self.encrypt
        inc32 = self._inc32
        for i in xrange(0, len(out), 16):
            mask = encrypt(counter)
            for j in xrange(i, min(len(out), i + 16)):
                out[j] = inp[j] ^ mask[j-i]
            inc32(counter)
        return out

    def _auth(self, ciphertext, ad, tagMask):
        y = 0
        y = self._update(y, ad)
        y = self._update(y, ciphertext)
        y ^= (len(ad) << (3 + 64)) | (len(ciphertext) << 3)
        y = self._mul(y)
        y ^= bytesToNumber(tagMask)
        return numberToByteArray(y, 16)

    def _update(self, y, data):
        for i in xrange(0, len(data) // 16):
            y ^= bytesToNumber(data[16*i:16*i+16])
            y = self._mul(y)
        extra = len(data) % 16
        if extra != 0:
            block = bytearray(16)
            block[:extra] = data[-extra:]
            y ^= bytesToNumber(block)
            y = self._mul(y)
        return y

    def _mul(self, y):
        """ Returns y*H, where H is the GCM key. """
        ret = 0
        # Multiply H by y 4 bits at a time, starting with the highest power
        # terms.
        gcmReductionTable = SPECK192GCM._gcmReductionTable
        productTable = self._productTable
        for i in xrange(0, 128, 4):
            # Multiply by x^4. The reduction for the top four terms is
            # precomputed.
            retHigh = ret & 0xf
            ret >>= 4
            ret ^= (gcmReductionTable[retHigh] << 112) # 128 - 16

            # Add in y' * H where y' are the next four terms of y, shifted down
            # to the x^0..x^4. This is one of the pre-computed multiples of
            # H. The multiplication by x^4 shifts them back into place.
            ret ^= productTable[y & 0xf]
            y >>= 4
        assert y == 0
        return ret

    def seal(self, nonce, plaintext, data):
        """
        Encrypts and authenticates plaintext using nonce and data. Returns the
        ciphertext, consisting of the encrypted plaintext and tag concatenated.
        """

        if len(nonce) != 12:
            raise ValueError("Bad nonce length")

        # The initial counter value is the nonce, followed by a 32-bit counter
        # that starts at 1. It's used to compute the tag mask.
        counter = bytearray(16)
        counter[:12] = nonce
        counter[-1] = 1
        tagMask = self.encrypt(counter)

        # The counter starts at 2 for the actual encryption.
        counter[-1] = 2
        
        ciphertext = self._rawSpeckCtrEncrypt(counter, plaintext)
 

        tag = self._auth(ciphertext, data, tagMask)

        return ciphertext + tag

    def open(self, nonce, ciphertext, data):
        """
        Decrypts and authenticates ciphertext using nonce and data. If the
        tag is valid, the plaintext is returned. If the tag is invalid,
        returns None.
        """

        if len(nonce) != 12:
            raise ValueError("Bad nonce length")
        if len(ciphertext) < 16:
            return None

        tag = ciphertext[-16:]
        ciphertext = ciphertext[:-16]

        # The initial counter value is the nonce, followed by a 32-bit counter
        # that starts at 1. It's used to compute the tag mask.
        counter = bytearray(16)
        counter[:12] = nonce
        counter[-1] = 1
        tagMask = self.encrypt(counter)

        if tag != self._auth(ciphertext, data, tagMask):
            return None

        # The counter starts at 2 for the actual decryption.
        counter[-1] = 2
        return self._rawSpeckCtrEncrypt(counter, ciphertext)

    @staticmethod
    def _reverseBits(i):
        assert i < 16
        i = ((i << 2) & 0xc) | ((i >> 2) & 0x3)
        i = ((i << 1) & 0xa) | ((i >> 1) & 0x5)
        return i

    @staticmethod
    def _gcmAdd(x, y):
        return x ^ y

    @staticmethod
    def _gcmShift(x):
        # Multiplying by x is a right shift, due to bit order.
        highTermSet = x & 1
        x >>= 1
        if highTermSet:
            # The x^127 term was shifted up to x^128, so subtract a 1+x+x^2+x^7
            # term. This is 0b11100001 or 0xe1 when represented as an 8-bit
            # polynomial.
            x ^= 0xe1 << (128-8)
        return x

    @staticmethod
    def _inc32(counter):
        for i in xrange(len(counter)-1, len(counter)-5, -1):
            counter[i] = (counter[i] + 1) % 256
            if counter[i] != 0:
                break
        return counter


    # define R(x, y, k) (x = ROR(x, 8), x += y, x ^= k, y = ROL(y, 3), y ^= x)

    def encrypt_round(self, x, y, k):
        #Feistel Operation       
        new_x = (((x << 56) | (x >> 8)) + y) & 18446744073709551615L
        new_x ^= k 
        new_y = ((y >> 61) | (y << 3))& 18446744073709551615L # y = ROL(y, 3)
        new_y ^= new_x

        return new_x, new_y


    def decrypt_round(self, x, y, k):
        #Inverse Feistel Operation

        xor_xy = x ^ y     
        new_y = ((xor_xy << 61) | (xor_xy >> 3))& 18446744073709551615L  # x = ROR_inv(xor_xy) 
        xor_xk = x ^ k

        msub = (xor_xk - new_y) & 18446744073709551615L
        new_x = ((msub >> 56) |(msub << 8))& 18446744073709551615L # y = ROL_inv(msub) 

        return new_x, new_y



    def encrypt(self, plaintext):        
  

        mod_mask = 18446744073709551615L

        blockBytesNum = bytesToNumber(plaintext)


        b = (blockBytesNum >> 64) & mod_mask   # shift by word_size 64
        a = blockBytesNum & mod_mask            

        keyschedule = self.key_schedule
        encrypt = self.encrypt_round

        for i in keyschedule:
            b, a = encrypt(b, a, i) 

        ciphertext = (b << 64) | a             # shift by word_size 64                  
        plaintextBytes= numberToByteArray(ciphertext,16) 


        return bytearray(plaintextBytes)


    def decrypt(self, ciphertext):

        mod_mask = 18446744073709551615L

        ciphertext = bytesToNumber(ciphertext)

        b = (ciphertext >> 64) & mod_mask     # shift by word_size 64   
        a = ciphertext & mod_mask       

        decrypt = self.decrypt_round
        key_schedule = self.key_schedule
        
        for i in reversed(key_schedule):
            b, a = decrypt(b, a, i)

        plaintext = (b << 64) | a            # shift by word_size 64   

        plaintext = numberToByteArray(plaintext,16)  
   

        return bytearray(plaintext)


    # _gcmReductionTable[i] is i * (1+x+x^2+x^7) for all 4-bit polynomials i. The
    # result is stored as a 16-bit polynomial. This is used in the reduction step to
    # multiply elements of GF(2^128) by x^4.
    _gcmReductionTable = [
        0x0000, 0x1c20, 0x3840, 0x2460, 0x7080, 0x6ca0, 0x48c0, 0x54e0,
        0xe100, 0xfd20, 0xd940, 0xc560, 0x9180, 0x8da0, 0xa9c0, 0xb5e0,
    ]
