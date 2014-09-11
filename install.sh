#Installation File
#Directory Rescue Crawler, direscraw v1.0
#Written by Brian Mikolajczyk, brianm12@gmail.com
#!/bin/bash
if [ -x $(which ddrescue) ]; then
cp direscraw /usr/local/bin
chmod a+x /usr/local/bin/direscraw
echo "direscraw installed successfully"
else
if [ -x $(which lzip ]; then
ddver=$(wget http://mirrors.kernel.org/gnu/ddrescue/ -qO - | grep -v sig | grep href | tail -1 | cut -d\> -f2 | cut -d\< -f1)
wget http://mirrors.kernel.org/gnu/ddrescue/$ddver
lzip -d $ddver
else sudo apt-get install lzip -y
fi

