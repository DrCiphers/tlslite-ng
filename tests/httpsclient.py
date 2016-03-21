#!/usr/bin/env python
from __future__ import print_function
from tlslite import HTTPTLSConnection, HandshakeSettings
from optparse import OptionParser


settings = HandshakeSettings()
settings.cipherNames = ['aes128gcm']
settings.keyExchangeNames = ['ecdhe_rsa']
settings.cipherImplementations = ["python"]
#settings.macNames = ['sha256']

settings.minVersion = (3,3)
settings.maxVersion = (3,3)   


settings.useExperimentalTackExtension = True

def main():

    parser = OptionParser(usage='%prog host filename [options]', description='A Simple https client used with tlslite-ng') 
    parser.add_option("--port", dest="port", help="port", default = 4443, type="int", metavar="4443")
    parser.add_option("--algo", dest="algo", help="algo", default = "speck128")
    parser.add_option("--keyEx", dest="keyEx", help="Key Exchange", default="ecdhe_rsa")
    
    (options, arguments) = parser.parse_args()
    
    if len(arguments) < 1:
        parser.print_help()
        exit(1)
        
        
    host = arguments[0]
        
    if (len(arguments)==1):
        filename="index.html"
    else:
        filename = arguments[1]
    
    
    port = options.port   
    algo = options.algo
    keyEx = options.keyEx
    
    settings.cipherNames = [algo]
    settings.keyExchangeNames = [keyEx]
    
    
    h = HTTPTLSConnection(host, port, settings=settings)    
    h.request("GET", filename)
    r = h.getresponse()
    print(r.read())


if __name__ == '__main__':
    main()
