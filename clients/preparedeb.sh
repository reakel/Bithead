#!/bin/bash
odir=$PWD
cd `dirname $0`
cd deb-install
if [ $1 ]
then
	echo $1 | grep -E '^[0-9.]+$' > /dev/null
	if [ $? = 0 ] 
	then 
		version=$1
	else
		echo Invalid version number
		exit 1
	fi
else
	currver=`cat DEBIAN/control | grep -i version | sed -r 's/^ *version: *([0-9.]+)$/\1/i'`;
	echo Please enter version number. Current version: $currver
	exit 1
fi
rm -r usr
mkdir usr
mkdir -p usr/bin
mkdir -p usr/sbin
mkdir -p usr/lib/python2.6/dist-packages

cp ../bhc-newuser.py usr/bin/bhc-newuser
cp ../bhc-realog.py usr/bin/bhc-realog
cp ../bhc-postinstall.py usr/sbin/bhc-postinstall
cp ../bhc-pubkey.py usr/sbin/bhc-pubkey
cp ../bhc-printers.py usr/sbin/bhc-printers

chmod -R 755 usr/bin/*
chmod -R 700 usr/sbin

cp -r ../bitheadclient usr/lib/python2.6/dist-packages/
sed -ri "s/^( *version: *)([0-9.]+)\$/\\1$version/i" DEBIAN/control
name="bithead-clients_$version"_all.deb
echo $name
cd ..
dpkg -b deb-install $odir/$name
