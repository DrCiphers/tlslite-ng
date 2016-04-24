#!/bin/bash

#aes128gcm speck128gcm  speck192gcm

if [ -z "$1"  ];
then
	ip="localhost"
else
	ip=$1
fi

echo "Performing Tests in the https server which resides in the $ip"

for fsize in 2MB 16MB 20MB 32MB; do

	for cipher in aes128 speck128 aes128gcm speck128gcm speck192gcm; do
		echo "Using $cipher"
       	
		for attempt in `seq 1 2` ; do
			
	       		echo "Performing attempt number $attempt with filesize $fsize"
			time ./httpsclient.py $ip index$fsize.html --algo=$cipher > /dev/null
		done
		echo " "
        done
	echo " "
	echo " "
done
