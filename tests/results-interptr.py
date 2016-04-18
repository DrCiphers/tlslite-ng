#!/usr/bin/env python
# Created by ioef - Efthimios Iosifidis 
# script that can calculate the mean values of the throughput 
# after multiple executions of the throughput-tests.script
# example: The script can interpret the following that one could execute
#
#          for NUM in `seq 1 20`; do ./throughput-tests.py client localhost:4443 . 2k; done >> results2k.txt 
#          for NUM in `seq 1 20`; do ./throughput-tests.py client localhost:4443 . 100k; done >> results100k.txt 
#          for NUM in `seq 1 20`; do ./throughput-tests.py client localhost:4443 . 500k; done >> results500k.txt        
#          for NUM in `seq 1 20`; do ./throughput-tests.py client localhost:4443 . 1MB ; done >> results2MB.txt
#          for NUM in `seq 1 20`; do ./throughput-tests.py client localhost:4443 . 2MB ; done >> results2MB.txt
#          for NUM in `seq 1 20`; do ./throughput-tests.py client localhost:4443 . 3MB ; done >> results3MB.txt

import math


def cleanListData(filename):
        cleanlist=[]
        for i in filename:
                if ( 'Test' in i) & ('good' not in i):
                        cleanlist.append(i)
                        
        numList=[]   
        for i in xrange(0,len(cleanlist)):
                numList.append(cleanlist[i].split()[9])        


        return numList



def Variance(numberList,meanValue,algo):

        val=0

        #steps 
        if algo=="aes128gcm":
                step=0
        elif algo=="aes128":
                step=1
        elif algo=="chacha20":
                step=4
        elif algo=="speck128":
                step=5
        elif algo=="speck128gcm":
                step=6
        elif algo=="speck192gcm":
                step=7        

        start=0
        resultval=0
        
        while start < len(numberList):
                retNum = int(numberList[step])
                val = (retNum-meanValue)
                val = val**2
                resultval += val
                step+=8
                start+=8                
        
        
        varNum = resultval/20
        
        return varNum

# Open the file handlers read the contents to a variable
# and close them.
#===============================================
fh1 = open("results2k.txt", "r")
fh2 = open("results100k.txt", "r")
fh3 = open("results500k.txt", "r")
fh4 = open("results1MB.txt", "r")
fh5 = open("results2MB.txt", "r")
fh6 = open("results3MB.txt", "r")


file1=fh1.readlines()
file2=fh2.readlines()
file3=fh3.readlines()
file4=fh4.readlines()
file5=fh5.readlines()
file6=fh6.readlines()


fh1.close()
fh2.close()
fh3.close()
fh4.close()
fh5.close()
fh6.close()


#Cleaning the data and keeping only the values 
#===============================================
                
numonly2k=[]   
numonly2k = cleanListData(file1)
        
numonly100k=[]   
numonly100k = cleanListData(file2)
        
numonly500k=[]   
numonly500k = cleanListData(file3)
        
numonly1MB=[]   
numonly1MB = cleanListData(file4)
        
numonly2MB=[]   
numonly2MB = cleanListData(file5)

numonly3MB=[]   
numonly3MB = cleanListData(file6)

        
#===============================================


a=0
b=1
c=4
d=5
e=6
f=7

aes128gcmval2k=0
aes128val2k=0
speck128val2k=0
chacha2k=0
speck128gcmval2k=0
speck192gcmval2k=0

aes128gcmval100k=0
aes128val100k=0
speck128val100k=0
chacha100k=0
speck128gcmval100k=0
speck192gcmval100k=0

aes128gcmval500k=0
aes128val500k=0
speck128val500k=0
chacha500k=0
speck128gcmval500k=0
speck192gcmval500k=0

aes128gcmval1MB=0
aes128val1MB=0
speck128val1MB=0
chacha1MB=0
speck128gcmval1MB=0
speck192gcmval1MB=0

aes128gcmval2MB=0
aes128val2MB=0
speck128val2MB=0
chacha2MB=0
speck128gcmval2MB=0
speck192gcmval2MB=0

aes128gcmval3MB=0
aes128val3MB=0
speck128val3MB=0
chacha3MB=0
speck128gcmval3MB=0
speck192gcmval3MB=0



while a < len(numonly2k):
    
        aes128gcmval2k += int(numonly2k[a])
        aes128val2k += int(numonly2k[b])
        chacha2k += int(numonly2k[c])
        speck128val2k += int(numonly2k[d])
        speck128gcmval2k += int(numonly2k[e])
        speck192gcmval2k += int(numonly2k[f])
    
    
        aes128gcmval100k += int(numonly100k[a])
        aes128val100k += int(numonly100k[b])
        chacha100k += int(numonly100k[c])
        speck128val100k += int(numonly100k[d])
        speck128gcmval100k += int(numonly100k[e])
        speck192gcmval100k += int(numonly100k[f])
        
        aes128gcmval500k += int(numonly500k[a])
        aes128val500k += int(numonly500k[b])
        chacha500k += int(numonly500k[c])
        speck128val500k += int(numonly500k[d])
        speck128gcmval500k += int(numonly500k[e])
        speck192gcmval500k += int(numonly500k[f])    

   
        aes128gcmval1MB += int(numonly1MB[a])
        aes128val1MB += int(numonly1MB[b])
        chacha1MB += int(numonly1MB[c])
        speck128val1MB += int(numonly1MB[d])
        speck128gcmval1MB += int(numonly1MB[e])
        speck192gcmval1MB += int(numonly1MB[f])

        aes128gcmval2MB += int(numonly2MB[a])
        aes128val2MB += int(numonly2MB[b])
        chacha2MB += int(numonly2MB[c])
        speck128val2MB += int(numonly2MB[d])
        speck128gcmval2MB += int(numonly2MB[e])
        speck192gcmval2MB += int(numonly2MB[f])
        
        aes128gcmval3MB += int(numonly3MB[a])
        aes128val3MB += int(numonly3MB[b])
        chacha3MB += int(numonly3MB[c])
        speck128val3MB += int(numonly3MB[d])
        speck128gcmval3MB += int(numonly3MB[e])
        speck192gcmval3MB += int(numonly3MB[f])        
    
        
        a += 8
        b += 8
        c += 8
        d += 8
        e += 8
        f += 8
        
#===============================================

    
length = 20
    
print("Average throughput of Algorithms when transferring 2kbytes of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval2k/length))
print("The Standard Deviation  of aes128gcm is:%s" %(Variance(numonly2k, aes128gcmval2k/length, "aes128gcm")**0.5))
print("Average Value of aes128python: %s bytes/sec"%(aes128val2k/length))
print("The Standard Deviation  of aes128python is:%s" %(Variance(numonly2k, aes128val2k/length, "aes128")**0.5))
print("Average Value of chacha20: %s bytes/sec"%(chacha2k/length))
print("The Standard Deviation  of chacha20 is:%s" %(Variance(numonly2k, chacha2k/length, "chacha20")**0.5))
print("Average Value of speck128: %s bytes/sec"%(speck128val2k/length))
print("The Standard Deviation  of speck128 is:%s" %(Variance(numonly2k, speck128val2k/length, "speck128")**0.5))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval2k/length))
print("The Standard Deviation  of speck128gcm is:%s" %(Variance(numonly2k, speck128gcmval2k/length, "speck128gcm")**0.5))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval2k/length))
print("The Standard Deviation  of speck192gcm is:%s" %(Variance(numonly2k, speck192gcmval2k/length, "speck192gcm")**0.5))


print(" ")
print("Average throughput of Algorithms when transferring 100k of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval100k/length))
print("The Standard Deviation  of aes128gcm is:%s" %(Variance(numonly100k, aes128gcmval100k/length, "aes128gcm")**0.5))
print("Average Value of aes128python: %s bytes/sec"%(aes128val100k/length))
print("The Standard Deviation  of aes128python is:%s" %(Variance(numonly100k, aes128val100k/length, "aes128")**0.5))
print("Average Value of chacha20: %s bytes/sec"%(chacha100k/length))
print("The Standard Deviation  of chacha20 is:%s" %(Variance(numonly100k, chacha100k/length, "chacha20")**0.5))
print("Average Value of speck128: %s bytes/sec"%(speck128val100k/length))
print("The Standard Deviation  of speck128 is:%s" %(Variance(numonly100k, speck128val100k/length, "speck128")**0.5))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval100k/length))
print("The Standard Deviation  of speck128gcm is:%s" %(Variance(numonly100k, speck128gcmval100k/length, "speck128gcm")**0.5))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval100k/length))
print("The Standard Deviation  of speck192gcm is:%s" %(Variance(numonly100k, speck192gcmval100k/length, "speck192gcm")**0.5))

print(" ")
print("Average throughput of Algorithms when transferring 500k of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval500k/length))
print("The Standard Deviation  of aes128gcm is:%s" %(Variance(numonly500k, aes128gcmval500k/length, "aes128gcm")**0.5))
print("Average Value of aes128python: %s bytes/sec"%(aes128val500k/length))
print("The Standard Deviation  of aes128python is:%s" %(Variance(numonly500k, aes128val500k/length, "aes128")**0.5))
print("Average Value of chacha20: %s bytes/sec"%(chacha500k/length))
print("The Standard Deviation  of chacha20 is:%s" %(Variance(numonly500k, chacha500k/length, "chacha20")**0.5))
print("Average Value of speck128: %s bytes/sec"%(speck128val500k/length))
print("The Standard Deviation  of speck128 is:%s" %(Variance(numonly500k, speck128val500k/length, "speck128")**0.5))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval500k/length))
print("The Standard Deviation  of speck128gcm is:%s" %(Variance(numonly500k, speck128gcmval500k/length, "speck128gcm")**0.5))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval500k/length))
print("The Standard Deviation  of speck192gcm is:%s" %(Variance(numonly500k, speck192gcmval500k/length, "speck192gcm")**0.5))

print(" ")
print("Average throughput of Algorithms when transferring 1MB of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval1MB/length))
print("The Standard Deviation  of aes128gcm is:%s" %(Variance(numonly1MB, aes128gcmval1MB/length, "aes128gcm")**0.5))
print("Average Value of aes128python: %s bytes/sec"%(aes128val1MB/length))
print("The Standard Deviation  of aes128python is:%s" %(Variance(numonly1MB, aes128val1MB/length, "aes128")**0.5))
print("Average Value of chacha20: %s bytes/sec"%(chacha1MB/length))
print("The Standard Deviation  of chacha20 is:%s" %(Variance(numonly1MB, chacha1MB/length, "chacha20")**0.5))
print("Average Value of speck128: %s bytes/sec"%(speck128val1MB/length))
print("The Standard Deviation  of speck128 is:%s" %(Variance(numonly1MB, speck128val1MB/length, "speck128")**0.5))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval1MB/length))
print("The Standard Deviation  of speck128gcm is:%s" %(Variance(numonly1MB, speck128gcmval1MB/length, "speck128gcm")**0.5))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval1MB/length))
print("The Standard Deviation  of speck192gcm is:%s" %(Variance(numonly1MB, speck192gcmval1MB/length, "speck192gcm")**0.5))


print(" ")
print("Average throughput of Algorithms when transferring 2MB of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval2MB/length))
print("The Standard Deviation  of aes128gcm is:%s" %(Variance(numonly2MB, aes128gcmval2MB/length, "aes128gcm")**0.5))
print("Average Value of aes128python: %s bytes/sec"%(aes128val2MB/length))
print("The Standard Deviation  of aes128python is:%s" %(Variance(numonly2MB, aes128val2MB/length, "aes128")**0.5))
print("Average Value of chacha20: %s bytes/sec"%(chacha2MB/length))
print("The Standard Deviation  of chacha20 is:%s" %(Variance(numonly2MB, chacha2MB/length, "chacha20")**0.5))
print("Average Value of speck128: %s bytes/sec"%(speck128val2MB/length))
print("The Standard Deviation  of speck128 is:%s" %(Variance(numonly2MB, speck128val2MB/length, "speck128")**0.5))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval2MB/length))
print("The Standard Deviation  of speck128gcm is:%s" %(Variance(numonly2MB, speck128gcmval2MB/length, "speck128gcm")**0.5))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval2MB/length))
print("The Standard Deviation  of speck192gcm is:%s" %(Variance(numonly2MB, speck192gcmval2MB/length, "speck192gcm")**0.5))

print(" ")
print("Average throughput of Algorithms when transferring 3MB of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval3MB/length))
print("The Standard Deviation  of aes128gcm is:%s" %(Variance(numonly3MB, aes128gcmval3MB/length, "aes128gcm")**0.5))
print("Average Value of aes128python: %s bytes/sec"%(aes128val3MB/length))
print("The Standard Deviation  of aes128python is:%s" %(Variance(numonly3MB, aes128val3MB/length, "aes128")**0.5))
print("Average Value of chacha20: %s bytes/sec"%(chacha3MB/length))
print("The Standard Deviation  of chacha20 is:%s" %(Variance(numonly3MB, chacha3MB/length, "chacha20")**0.5))
print("Average Value of speck128: %s bytes/sec"%(speck128val3MB/length))
print("The Standard Deviation  of speck128 is:%s" %(Variance(numonly3MB, speck128val3MB/length, "speck128")**0.5))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval3MB/length))
print("The Standard Deviation  of speck128gcm is:%s" %(Variance(numonly3MB, speck128gcmval3MB/length, "speck128gcm")**0.5))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval3MB/length))
print("The Standard Deviation  of speck192gcm is:%s" %(Variance(numonly3MB, speck192gcmval3MB/length, "speck192gcm")**0.5))
print(" ")
