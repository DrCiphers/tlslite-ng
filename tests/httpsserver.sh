#!/bin/sh
if [ -z "$1" ]; then
        python ../scripts/tls.py server -k serverX509Key.pem -c serverX509Cert.pem -t TACK1.pem localhost:4443
else
        python ../scripts/tls.py server -k serverX509Key.pem -c serverX509Cert.pem -t TACK1.pem $1:4443
fi

