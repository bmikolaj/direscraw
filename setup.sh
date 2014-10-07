#!/bin/bash
#Setup File
#Directory Rescue Crawler, direscraw v1.4; Error Percentage and Runtime Calculation Summary, errcalc v1.0
#Copyright (c) 2014 by Brian Mikolajczyk, brianm12@gmail.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

if [ $1 == "install" ]; then
	if [ ! -x $(which lzip) ]; then
		lver=$(wget http://download.savannah.gnu.org/releases/lzip/ -qO - | grep lzip | grep -v plzip | grep tar.gz | grep -v sig | cut -d\" -f8 | tail -1)
		wget -q http://download.savannah.gnu.org/releases/lzip/$lver
		gunzip $lver
		tar xf "${lver%.gz}"
		cd "${lver%.tar.gz}"
		./configure && make && sudo make install
		cd ..
	fi
	if [ ! -x $(which ddrescue) ]; then
		ddver=$(wget http://mirrors.kernel.org/gnu/ddrescue/ -qO - | grep -v sig | grep href | tail -1 | cut -d\> -f2 | cut -d\< -f1)
		wget -q http://mirrors.kernel.org/gnu/ddrescue/$ddver
		lzip -d $ddver
		tar xf "${ddver%.lz}"
		cd "${ddver%.tar.lz}"
		./configure && make && sudo make install
		cd ..
	fi
	if [ ! -x $(which units) ]; then
		unvar=$(wget http://ftp.gnu.org/gnu/units/ -qO - | grep -v sig | grep href | grep units | tail -1 | cut -d\" -f6)
		wget -q http://ftp.gnu.org/gnu/units/$unvar
		gunzip $unvar
		tar xf "${unvar%.gz}"
		cd "${unvar%.tar.gz}"
		./configure && make && sudo make install
		cd ..
	fi
	sudo cp errcalc /usr/local/bin
	sudo cp direscraw.py /usr/local/bin/direscraw
	sudo chmod a+x /usr/local/bin/direscraw
	sudo chmod a+x /usr/local/bin/errcalc
	echo "direscraw and errcalc installed successfully"
elif [[ $1 == "uninstall" ]]; then
	sudo rm /usr/local/bin/errcalc /usr/local/bin/direscraw
	echo "direscraw and errcalc uninstalled successfully"
else
	echo "Usage"
	echo "'sudo ./setup.sh install' to install"
	echo "'sudo ./setup.sh uninstall' to uninstall"
fi
