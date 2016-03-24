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
        self.name = 'speck128'
        
        self.block_size = 16      #16bytes x 8bits = 128 bits 
        
        #convert the key bytesarray to int
        self.key = self.bytesToNumber(key)
        self.IV = IV
        

        
        # Create Properly Sized bit mask for truncating addition and left shift outputs          
        self.mod_mask = (2 ** 64) - 1  # word_size = 64    alpha_shift = 8 , beta_shift = 3
        
        
        
        # Parse the given key and truncate it to the key length
        try:
            self.key = self.key & ((2 ** 128) - 1)
        except (ValueError, TypeError):
            print('Invalid Key Value!')
            print('Please Provide Key as int')
            raise

        # Pre-compile key schedule
        self.key_schedule = [self.key & self.mod_mask]
        l_schedule = [(self.key >> (x * 64)) & self.mod_mask for x in xrange(1, 128 // 64)]

        encrypt_round = self.encrypt_round
        
        for x in xrange(31): # rounds - 1 
            new_l_k = encrypt_round(l_schedule[x], self.key_schedule[x], x)
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
        

        bytesToNumber = self.bytesToNumber
        numberToByteArray = self.numberToByteArray
        keyschedule = self.key_schedule
        encryptround = self.encrypt_round  

        #CBC Mode: For each block...
        for x in xrange(len(plaintextBytes)//16):
            
            #XOR with the chaining block
            blockBytes = plaintextBytes[x*16 : (x*16)+16]
        
            for y in xrange(16):
                blockBytes[y] ^= chainBytes[y]
               
            blockBytesNum = bytesToNumber(blockBytes)

            b = (blockBytesNum >> 64) & mod_mask   # blockBytesNum >> self.wordsize 
            a = blockBytesNum & mod_mask           
            
            for i in keyschedule:
                b, a = encryptround(b, a, i) 
        
            ciphertext = (b << 64) | a           # b << self.wordsize                      
            ciphertext= numberToByteArray(ciphertext)           
            
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

        bytesToNumber = self.bytesToNumber
        numberToByteArray = self.numberToByteArray
        decryptround = self.decrypt_round
        key_schedule = self.key_schedule        

        #CBC Mode: For each block...
        for x in xrange(len(ciphertextBytes)//16):

            #Decrypt it
            blockBytes = ciphertextBytes[x*16 : (x*16)+16]
               
            ciphertext = bytesToNumber(blockBytes)
        
            b = (ciphertext >> 64) & mod_mask
            a = ciphertext & mod_mask       
              
            for i in reversed(key_schedule):
                b, a = decryptround(b, a, i)
          
            plaintext = (b << 64) | a                 
            plaintext = numberToByteArray(plaintext)  
            
            #XOR with the chaining block and overwrite the input with output
            for y in xrange(16):
                plaintext[y] ^= chainBytes[y]
                ciphertextBytes[(x*16)+y] = plaintext[y]
            
            #Set the next chaining block
            chainBytes = blockBytes

        self.IV = chainBytes[:]
        
        return bytearray(ciphertextBytes)
