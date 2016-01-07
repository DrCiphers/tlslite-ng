# Pure-Python Speck implementation Class.
# Authors: 
#   Efthimios Iosifidis
#
# See the LICENSE file for legal information regarding use of this file.

def new(key, IV):
    return Python_SPECK(key, IV)

class Python_SPECK():
    
    def __init__(self, key, IV):
        
        self.isBlockCipher = True
        self.isAEAD = False
        self.implementation = 'python'
        self.name = 'speck'
        
        self.block_size = 16      #16bytes x 8bits = 128 bits 
        
        #convert the key bytesarray to int
        self.key = self.bytesToNumber(key)
        
        self.IV = IV
        self.rounds = 32
        self.word_size = 64         # alpha_shift = 8 , beta_shift = 3
    
        # Create Properly Sized bit mask for truncating addition and left shift outputs          
        self.mod_mask = (2 ** self.word_size) - 1 
   
        # Parse the given key and truncate it to the key length
        try:
            self.key = self.key & ((2 ** 128) - 1)
        except (ValueError, TypeError):
            print('Invalid Key Value!')
            print('Please Provide Key as int')
            raise

        # Pre-compile key schedule
        self.key_schedule = [self.key & self.mod_mask]
        l_schedule = [(self.key >> (x * self.word_size)) & self.mod_mask for x in xrange(1, 128 // self.word_size)]

        for x in xrange(self.rounds - 1):
            new_l_k = self.encrypt_round(l_schedule[x], self.key_schedule[x], x)
            l_schedule.append(new_l_k[0])
            self.key_schedule.append(new_l_k[1])

    def bytesToNumber(self,b):
        total = 0
        multiplier = 1
        for count in xrange(len(b)-1, -1, -1):
            byte = b[count]
            total += multiplier * byte
            multiplier *= 256
        return total

    def numberToByteArray(self,n):
        """Convert an integer into a bytearray, zero-pad to 16 Bytes.
    
        The returned bytearray may be smaller than howManyBytes, but will
        not be larger.  The returned bytearray will contain a big-endian
        encoding of the input integer (n).
        """    
        b = bytearray(16)
        for count in xrange(15, -1, -1):
            b[count] = int(n % 256)
            n >>= 8
        return b

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
        
        plaintextBytes = plaintext[:]
        chainBytes = self.IV[:]      
        
        mod_mask = 18446744073709551615L

        #CBC Mode: For each block...
        for x in xrange(len(plaintextBytes)//16):

            #XOR with the chaining block
            blockBytes = plaintextBytes[x*16 : (x*16)+16]
        
            for y in xrange(16):
                blockBytes[y] ^= chainBytes[y]
               
            blockBytesNum = self.bytesToNumber(blockBytes)

            
            b = (blockBytesNum >> self.word_size) & mod_mask
            a = blockBytesNum & mod_mask            
           
            keyschedule = self.key_schedule
            encrypt = self.encrypt_round
            
            for i in keyschedule:
                b, a = encrypt(b, a, i) 

                
            ciphertext = (b << self.word_size) | a                             
            ciphertext= self.numberToByteArray(ciphertext) 
                        
            #Overwrite the input with the output
            for y in xrange(16):
                plaintextBytes[(x*16)+y] = ciphertext[y]

            #Set the next chaining block
            chainBytes = ciphertext

        self.IV = chainBytes[:]
        return bytearray(plaintextBytes)

    def decrypt(self, ciphertext):
 
        ciphertextBytes = ciphertext[:]
        chainBytes = self.IV[:]

        mod_mask = 18446744073709551615L

        #CBC Mode: For each block...
        for x in xrange(len(ciphertextBytes)//16):
            #Decrypt it
            blockBytes = ciphertextBytes[x*16 : (x*16)+16]
               
            ciphertext = self.bytesToNumber(blockBytes)
        
            b = (ciphertext >> self.word_size) & mod_mask
            a = ciphertext & mod_mask       
           
            decrypt = self.decrypt_round
            for i in reversed(self.key_schedule):
                b, a = decrypt(b, a, i)
          
            plaintext = (b << self.word_size) | a    
                
            plaintext = self.numberToByteArray(plaintext)  
            
            #XOR with the chaining block and overwrite the input with output
            for y in xrange(16):
                plaintext[y] ^= chainBytes[y]
                ciphertextBytes[(x*16)+y] = plaintext[y]
            
            #Set the next chaining block
            chainBytes = blockBytes

        self.IV = chainBytes[:]
        return bytearray(ciphertextBytes)
