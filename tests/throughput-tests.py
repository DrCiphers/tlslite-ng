#!/usr/bin/python

# Authors: 
#   Trevor Perrin
#   Hubert Kario 
#   Efthimios Iosifidis - Based on the code from the initial authors
#   transformed the test file in order to perfom throughput tests amongst
#   the AES, the RC4, the Chacha20 and the Speck Cipher 
#   
# See the LICENSE file for legal information regarding use of this file.


from __future__ import print_function


import sys
import os
import os.path
import socket
import time
import getopt
from tlslite.constants import CipherSuite

try:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
except ImportError:
    from http.server import HTTPServer, SimpleHTTPRequestHandler

from tlslite import TLSConnection, Fault, HandshakeSettings, \
    X509, X509CertChain, IMAP4_TLS, VerifierDB, Session, SessionCache, \
    parsePEMKey, constants, \
    AlertDescription, HTTPTLSConnection, TLSSocketServerMixIn, \
    POP3_TLS, m2cryptoLoaded, pycryptoLoaded, gmpyLoaded, tackpyLoaded, \
    Checker, __version__

from tlslite.errors import *
from tlslite.utils.cryptomath import prngName
try:
    import xmlrpclib
except ImportError:
    # Python 3
    from xmlrpc import client as xmlrpclib
import ssl
from tlslite import *

try:
    from tack.structures.Tack import Tack
    
except ImportError:
    pass

def printUsage(s=None):
    if m2cryptoLoaded:
        crypto = "M2Crypto/OpenSSL"
    else:
        crypto = "Python crypto"        
    if s:
        print("ERROR: %s" % s)
    print("""\ntls.py version %s (using %s)  

Commands:
  server HOST:PORT DIRECTORY DATASIZE

  client HOST:PORT DIRECTORY DATASIZE
""" % (__version__, crypto))
    sys.exit(-1)
    

def dataRandomizer(datasize):
           
    if datasize == "3MB":
        data = os.urandom(1500000)    
        
    elif datasize == "2MB":
        data = os.urandom(1000000)
        
    elif datasize == "1MB":
        data = os.urandom(500000)
        
    elif datasize == "500k":
        data = os.urandom(250000)
    
    elif datasize == "100k":
        data = os.urandom(50000)
    
    elif datasize == "2k":
        data = os.urandom(1000)
    else:
        return 0
        
    return  data


def clientTestCmd(argv):
    
    address = argv[0]
    dir = argv[1]    
    datasize = argv[2]
    
    
    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #open synchronisation FIFO
    synchro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    synchro.settimeout(40)
    synchro.connect((address[0], address[1]-1))

    def connect():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if hasattr(sock, 'settimeout'): #It's a python 2.3 feature
            sock.settimeout(25)
        sock.connect(address)
        c = TLSConnection(sock)
        return c

    test_no = 0

    badFault = False
 
    message = dataRandomizer(datasize) 
 
    for cipher in [ "aes128gcm","aes128", "aes256",
                       "rc4", "chacha20-poly1305", "speck128", "speck128gcm","speck192gcm"]:                   
        test_no += 1

        t1 = time.time()
        print("Test {0}:".format(test_no), end=' ')
        synchro.recv(1)
        connection = connect()

        t2 = time.time()

        settings = HandshakeSettings()
        settings.cipherNames = [cipher]
        settings.cipherImplementations = ["python"]
        connection.handshakeClientCert(settings=settings)
        t3 = time.time()
        print("%s %s:" % (connection.getCipherName(), connection.getCipherImplementation()), end=' ')


        if datasize == "3MB":
            t3 = time.time()
            connection.write(message)
            h = connection.read(min=1500000, max=1500000)
            t4 = time.time()                
            if t4-t3:
                print("3MB exchanged at rate of %d bytes/sec" % int(3000000/(t4-t3)))
		print ('Raw timers:','t1=', t1,'t2=', t2,'t3=', t3,'t4=', t4)
                print ('Intervals:', t2-t1, t3-t2, t4-t3)
		sizeInBytes = sys.getsizeof(h)*2
                print("Tranmsitted data size:", sizeInBytes)
		print("Throughput is bytes/sec:", round(sizeInBytes / (t4-t3), 3))

            else:
                print("3MB exchanged very fast")
                            
            assert(h == message)            

        elif datasize == "2MB":
            t3 = time.time()
            connection.write(message)
            h = connection.read(min=1000000, max=1000000)
            t4 = time.time()                
            if t4-t3:
                print("2MB exchanged at rate of %d bytes/sec" % int(2000000/(t4-t3)))
		print ('Raw timers:','t1=', t1,'t2=', t2,'t3=', t3,'t4=', t4)
		print ('Intervals:', t2-t1, t3-t2, t4-t3)
		sizeInBytes = sys.getsizeof(h)*2
		print("Tranmsitted data size:", sizeInBytes)
		print("Throughput:", round(sizeInBytes / (t4-t3), 3))		
            else:
                print("2MB exchanged very fast")
                
            assert(h == message)
                
        elif datasize == "1MB": 
            t3 = time.time()
            connection.write(message)
            h = connection.read(min=500000, max=500000)
            t4 = time.time()
            if t4-t3:
                print("1MB exchanged at rate of %d bytes/sec" % int(1000000/(t4-t3)))
                print ('Raw timers:','t1=', t1,'t2=', t2,'t3=', t3,'t4=', t4)
                print ('Intervals:', t2-t1, t3-t2, t4-t3)
		sizeInBytes = sys.getsizeof(h)*2
                print("Tranmsitted data size:", sizeInBytes)
		print("Throughput:", round(sizeInBytes / (t4-t3), 3))
            else:
                print("1MB exchanged very fast")
            
            assert(h == message)                

        elif datasize == "500k":
	    t3 = time.time()
            connection.write(message)
            h = connection.read(min=250000, max=250000)
	    t4 = time.time()
            if t4-t3:
                print("500kbytes exchanged at rate of %d bytes/sec" % int(500000/(t4-t3)))
		print ('Raw timers:','t1=', t1,'t2=', t2,'t3=', t3,'t4=', t4)
		print ('Intervals:', t2-t1, t3-t2, t4-t3)
		sizeInBytes = sys.getsizeof(h)*2
		print("Tranmsitted data size:", sizeInBytes)
		print("Throughput:", round(sizeInBytes / (t4-t3), 3))		
            else:
                print("500kbytes exchanged very fast")
    
            assert(h == message)                                               
             
        elif datasize == "100k":
            t3 = time.time()
            connection.write(message)
            h = connection.read(min=50000, max=50000)
            t4 = time.time()
            if t4-t3:
                print("100kBytes exchanged at rate of %d bytes/sec" % int(100000/(t4-t3)))
		print ('Raw timers:','t1=', t1,'t2=', t2,'t3=', t3,'t4=', t4)
		print ('Intervals:', t2-t1, t3-t2, t4-t3)
		sizeInBytes = sys.getsizeof(h)*2
		print("Tranmsitted data size:", sizeInBytes)
		print("Throughput:", round(sizeInBytes / (t4-t3), 3))		
            else:
                print("100kBytes exchanged very fast")
                
            assert(h == message)                
                
        elif datasize == "2k":  
            t3 = time.time()
            connection.write(message)
            h = connection.read(min=1000, max=1000)
	    t4 = time.time()
            if t4-t3:
                print("2kBytes exchanged at rate of %d bytes/sec" % int(2000/(t4-t3)))
		print ('Raw timers:','t1=', t1,'t2=', t2,'t3=', t3,'t4=', t4)
		print ('Intervals:', t2-t1, t3-t2, t4-t3)
		sizeInBytes = sys.getsizeof(h)*2
		print("Tranmsitted data size:", sizeInBytes)
		print("Throughput:", round(sizeInBytes / (t4-t3), 3))		
            else:
                print("2kBytes exchanged very fast")
            
            assert(h == message)                
                
        else:
            print("Datasize not supported or syntax error! Exiting...")
            exit(1)
                

        print("Used Ciphersuite: {0}".\
                format(CipherSuite.ietfNames[connection.session.cipherSuite]))            
            
        print(" ")
        connection.close()

    synchro.close()

    if not badFault:
        print("Test succeeded, {0} good".format(test_no))
    else:
        print("Test failed")



def testConnServer(connection):
    count = 0
    while 1:
        s = connection.read()
        count += len(s)
        if len(s) == 0:
            break
        connection.write(s)
        if count == 1111:
            break

def serverTestCmd(argv):

    address = argv[0]
    dir = argv[1]
    datasize = argv[2]
    
    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #Create synchronisation FIFO
    synchroSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    synchroSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    synchroSocket.bind((address[0], address[1]-1))
    synchroSocket.listen(2)

    #Connect to server
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind(address)
    lsock.listen(5)

    # following is blocking until the other side doesn't open
    synchro = synchroSocket.accept()[0]


    def connect():
        return TLSConnection(lsock.accept()[0])

    x509Cert = X509().parse(open(os.path.join(dir, "serverX509Cert.pem")).read())
    x509Chain = X509CertChain([x509Cert])
    s = open(os.path.join(dir, "serverX509Key.pem")).read()
    x509Key = parsePEMKey(s, private=True)

    test_no = 0
    

    for cipher in ["aes128gcm", "aes128", "aes256", "rc4","chacha20-poly1305","speck128", "speck128gcm", "speck192gcm"]:
       
        test_no += 1

        print("Test {0}:".format(test_no), end=' ')
        synchro.send(b'R')
        connection = connect()

        settings = HandshakeSettings()
        settings.cipherNames = [cipher]
        settings.cipherImplementations = ["python"]

        connection.handshakeServer(certChain=x509Chain, privateKey=x509Key,
                                        settings=settings)
        print(connection.getCipherName(), connection.getCipherImplementation())
            
        if datasize == "3MB":
            h = connection.read(min=1500000, max=1500000)             

        elif datasize == "2MB":
            h = connection.read(min=1000000, max=1000000) 
                
        elif datasize == "1MB":
            h = connection.read(min=500000, max=500000)         

        elif datasize == "500k":
            h = connection.read(min=250000, max=250000)
                
        elif datasize == "100k":
                h = connection.read(min=50000, max=50000)
                
        elif datasize == "2k":
            h = connection.read(min=1000, max=1000)
            
        else:  
                
            print("Datasize not supported or syntax error! Exiting...")
            exit(1)

            
            
        connection.write(h)
        connection.close()




    synchro.close()
    synchroSocket.close()

    print("Test succeeded")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        printUsage("Missing command")
    elif sys.argv[1] == "client"[:len(sys.argv[1])]:
        clientTestCmd(sys.argv[2:])
    elif sys.argv[1] == "server"[:len(sys.argv[1])]:
        serverTestCmd(sys.argv[2:])
    else:
        printUsage("Unknown command: %s" % sys.argv[1])
