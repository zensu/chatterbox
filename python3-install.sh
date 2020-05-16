#!/bin/bash

wget https://python.org/ftp/python/3.7.2/Python-3.7.2.tgz
tar xzf Python-3.7.2.tgz &>/dev/null

cd Python-3.7.2
./configure --enable-optimizations --with-ensurepip=install
echo "<<<MAKE INSTALL>>>"
make install

