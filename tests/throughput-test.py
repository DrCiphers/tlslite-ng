#!/usr/bin/env python

# Authors: 
#   Trevor Perrin
#   Kees Bos - Added tests for XML-RPC
#   Dimitris Moraitis - Anon ciphersuites
#   Marcelo Fernandez - Added test for NPN
#   Martin von Loewis - python 3 port
#   Hubert Kario - several improvements
#   Google - FALLBACK_SCSV test
#   Efthimios Iosifidis - Added Speck Cipher 
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
  server HOST:PORT DIRECTORY

  client HOST:PORT DIRECTORY
""" % (__version__, crypto))
    sys.exit(-1)
    

def testConnClient(conn):
    b1 = os.urandom(1)
    b10 = os.urandom(10)
    b100 = os.urandom(100)
    b1000 = os.urandom(1000)
    conn.write(b1)
    conn.write(b10)
    conn.write(b100)
    conn.write(b1000)
    assert(conn.read(min=1, max=1) == b1)
    assert(conn.read(min=10, max=10) == b10)
    assert(conn.read(min=100, max=100) == b100)
    assert(conn.read(min=1000, max=1000) == b1000)

def clientTestCmd(argv):
    
    address = argv[0]
    dir = argv[1]    

    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #open synchronisation FIFO
    synchro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    synchro.settimeout(25)
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
 
    implementations = []
    if m2cryptoLoaded:
        implementations.append("openssl")
    if pycryptoLoaded:
        implementations.append("pycrypto")
    implementations.append("python") 
 
    for implementation in ['python']:
        for cipher in ["aes128gcm", "aes128", "aes256", "3des",
                       "rc4", "chacha20-poly1305", "speck128", "speck128gcm","speck192gcm"]:
            # skip tests with implementations that don't support them
            if cipher == "3des" and implementation not in ("openssl",
                                                           "pycrypto"):
                continue
            if cipher in ("aes128gcm", "aes256gcm") and \
                    implementation not in ("pycrypto",
                                           "python"):
                continue
            if cipher in ("chacha20-poly1305", ) and \
                    implementation not in ("python", ):
                continue
            
            if cipher == "speck128" and \
                    implementation not in ("python"):
                continue            

            test_no += 1

            print("Test {0}:".format(test_no), end=' ')
            synchro.recv(1)
            connection = connect()

            settings = HandshakeSettings()
            settings.cipherNames = [cipher]
            settings.cipherImplementations = [implementation, "python"]
            connection.handshakeClientCert(settings=settings)
            print("%s %s:" % (connection.getCipherName(), connection.getCipherImplementation()), end=' ')

            startTime = time.clock()
            connection.write(b"hello"*100000)
            h = connection.read(min=500000, max=500000)
            stopTime = time.clock()
            if stopTime-startTime:
                print("1MB exchanged at rate of %d bytes/sec" % int(1000000/(stopTime-startTime)))
            else:
                print("1MB exchanged very fast")

            assert(h == b"hello"*100000)

            print(" Used Ciphersuite: {0}".\
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

   
    implementations = []
    if m2cryptoLoaded:
        implementations.append("openssl")
    if pycryptoLoaded:
        implementations.append("pycrypto")
    implementations.append("python")   


    for implementation in ['python']:
        for cipher in ["aes128gcm", "aes128", "aes256", "3des",
                       "rc4","chacha20-poly1305","speck128", "speck128gcm", "speck192gcm"]:
            # skip tests with implementations that don't support them
            if cipher == "3des" and implementation not in ("openssl",
                                                           "pycrypto"):
                continue
            if cipher in ("aes128gcm", "aes256gcm") and \
                    implementation not in ("pycrypto",
                                           "python"):
                continue
            if cipher in ("chacha20-poly1305", ) and \
                    implementation not in ("python", ):
                continue
            
            if cipher == "speck128" and \
                    implementation not in ("python"):
                continue

            test_no += 1

            print("Test {0}:".format(test_no), end=' ')
            synchro.send(b'R')
            connection = connect()

            settings = HandshakeSettings()
            settings.cipherNames = [cipher]
            settings.cipherImplementations = [implementation, "python"]

            connection.handshakeServer(certChain=x509Chain, privateKey=x509Key,
                                        settings=settings)
            print(connection.getCipherName(), connection.getCipherImplementation())
            h = connection.read(min=500000, max=500000)
            assert(h == b"hello"*100000)
            connection.write(h)
            connection.close()




    synchro.close()
    synchroSocket.close()

    print("Test succeeded")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        printUsage("Missing command")
    elif sys.argv[1] == "client"[:len(sys.argv[1])]:
        clientTestCmd(sys.argv[2:])
    elif sys.argv[1] == "server"[:len(sys.argv[1])]:
        serverTestCmd(sys.argv[2:])
    else:
        printUsage("Unknown command: %s" % sys.argv[1])
