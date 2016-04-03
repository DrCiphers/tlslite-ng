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


def cleanListData(filename):
        cleanlist=[]
        for i in filename:
                if ( 'Test' in i) & ('good' not in i):
                        cleanlist.append(i)
                        
        numList=[]   
        for i in xrange(0,len(cleanlist)):
                numList.append(cleanlist[i].split()[9])        


        return numList




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
file7=fh7.readlines()


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
print("Average Value of aes128python: %s bytes/sec"%(aes128val2k/length))
print("Average Value of chacha20: %s bytes/sec"%(chacha2k/length))
print("Average Value of speck128: %s bytes/sec"%(speck128val2k/length))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval2k/length))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval2k/length))


print(" ")
print("Average throughput of Algorithms when transferring 100k of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval100k/length))
print("Average Value of aes128python: %s bytes/sec"%(aes128val100k/length))
print("Average Value of chacha20: %s bytes/sec"%(chacha100k/length))
print("Average Value of speck128: %s bytes/sec"%(speck128val100k/length))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval100k/length))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval100k/length))

print(" ")
print("Average throughput of Algorithms when transferring 500k of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval500k/length))
print("Average Value of aes128python: %s bytes/sec"%(aes128val500k/length))
print("Average Value of chacha20: %s bytes/sec"%(chacha500k/length))
print("Average Value of speck128: %s bytes/sec"%(speck128val500k/length))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval500k/length))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval500k/length))

print(" ")
print("Average throughput of Algorithms when transferring 1MB of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval1MB/length))
print("Average Value of aes128python: %s bytes/sec"%(aes128val1MB/length))
print("Average Value of chacha20: %s bytes/sec"%(chacha1MB/length))
print("Average Value of speck128: %s bytes/sec"%(speck128val1MB/length))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval1MB/length))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval1MB/length))

print(" ")
print("Average throughput of Algorithms when transferring 2MB of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval2MB/length))
print("Average Value of aes128python: %s bytes/sec"%(aes128val2MB/length))
print("Average Value of chacha20: %s bytes/sec"%(chacha2MB/length))
print("Average Value of speck128: %s bytes/sec"%(speck128val2MB/length))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval2MB/length))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval2MB/length))

print(" ")
print("Average throughput of Algorithms when transferring 3MB of data")
print("Average Value of aes128gcm: %s bytes/sec"%(aes128gcmval3MB/length))
print("Average Value of aes128python: %s bytes/sec"%(aes128val3MB/length))
print("Average Value of chacha20: %s bytes/sec"%(chacha3MB/length))
print("Average Value of speck128: %s bytes/sec"%(speck128val3MB/length))
print("Average Value of speck128gcm: %s bytes/sec"%(speck128gcmval3MB/length))
print("Average Value of speck192gcm: %s bytes/sec"%(speck192gcmval3MB/length))
