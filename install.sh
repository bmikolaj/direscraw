#!/bin/bash
#Installation File
#Directory Rescue Crawler, direscraw v1.0
#Written by Brian Mikolajczyk, brianm12@gmail.com
if [ ! -x $(which lzip ]; then
lver=$(wget http://download.savannah.gnu.org/releases/lzip/ -qO - | grep lzip | grep -v plzip | grep tar.gz | grep -v sig | cut -d\" -f8 | tail -1)
wget -q http://download.savannah.gnu.org/releases/lzip/$lver
gunzip $lver
tar xf "${lver%.gz}"
cd "${lver%.tar.gz}"
./configure
make
sudo make install
cd ..
fi
if [ ! -x $(which ddrescue) ]; then
ddver=$(wget http://mirrors.kernel.org/gnu/ddrescue/ -qO - | grep -v sig | grep href | tail -1 | cut -d\> -f2 | cut -d\< -f1)
wget -q http://mirrors.kernel.org/gnu/ddrescue/$ddver
lzip -d $ddver
tar xf "${ddver%.lz}"
cd "${ddver%.tar.lz}"
./configure
make
sudo make install
cd ..
fi
cp direscraw /usr/local/bin
chmod a+x /usr/local/bin/direscraw
echo "direscraw installed successfully"
