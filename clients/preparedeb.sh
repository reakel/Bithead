#!/bin/bash
odir=$PWD
cd `dirname $0`
cd deb-install
rm -r usr
mkdir usr
mkdir -p usr/bin
mkdir -p usr/sbin
mkdir -p usr/lib/pymodules/python2.6

cp ../bhc-newuser.py usr/bin/bhc-newuser
cp ../bhc-realog.py usr/bin/bhc-realog
cp ../bhc-postinstall.py usr/sbin/bhc-postinstall
cp ../bhc-pubkey.py usr/sbin/bhc-pubkey

chmod 755 usr/bin/*
chmod 700 usr/sbin

cp -r ../bitheadclient usr/lib/pymodules/python2.6/
version=`grep "Version:" < DEBIAN/control | sed -E 's/^ *Version: *([0-9\.]+)$/\1/'`
name="bithead-clients_$version"_all.deb
echo $name
cd ..
dpkg -b deb-install $odir/$name
