#!/usr/bin/env python
from __future__ import print_function
from tlslite import HTTPTLSConnection, HandshakeSettings
from optparse import OptionParser


settings = HandshakeSettings()
#settings.cipherNames = ['speck']
settings.keyExchangeNames = ['dhe_rsa']
settings.cipherImplementations = ["python"]
settings.macNames = ['sha256']

settings.minVersion = (3,3)
settings.maxVersion = (3,3)   


settings.useExperimentalTackExtension = True

def main():

    parser = OptionParser(usage='%prog host [options]', description='A Simple https client used with tlslite-ng') 
    parser.add_option("--port", dest="port", help="port", default = 4443, type="int", metavar="4443")
    parser.add_option("--algo", dest="algo", help="algo", default = "speck")
    
    (options, arguments) = parser.parse_args()
    
    if len(arguments) < 1:
        parser.print_help()
        exit(1)
        
    host = arguments[0]
    port = options.port   
    algo = options.algo
    settings.cipherNames = [algo]
    
    
    h = HTTPTLSConnection(host, port, settings=settings)    
    h.request("GET", "/index.html")
    r = h.getresponse()
    print(r.read())


if __name__ == '__main__':
    main()

