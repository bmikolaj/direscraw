#Directory Rescue Crawler
v1.0

##Description

Directory Rescue Crawler uses `ddrescue` to recover full directories from one location to another. This program also prints a error and runtime summary in each directory copied and a full summary in the root directory.

##Dependencies
Directory Rescue Crawler was designed for Linux and uses the following programs.

* Bash
* Python 2.7+
* Gunzip
* Tar
* Lzip (installed via install.sh)
* Ddrescue (installed via install.sh)
* GNU Units (installed via install.sh)

##Install
Run the following command to install;

`sudo ./install.sh`

This will install two programs: Directory Rescue Crawler (`direscraw`) and the Error Percentage and Runtime Calculation Summary (`errcalc`) to /usr/local/bin.

##Usage
Run from the command line;

`direscraw [-h] <input_directory> <output_directory> [-b] BLACKLIST`

####Required parameters
`<input_directory>` and `<output_directory>` are required.
####Optional parameters
`-h` for help

`-b BLACKLIST` specifies a list of files and/or directories separated by a space to omit from rescuing (case-sensitive). 

###Example 
`use@computer:$ direscraw /media/Drive1/ /media/Drive2/Backup/ -b .mp3 'Pictures Of Me'` (This will omit all mp3 files and a directory called Pictures Of Me). 

Note: Directories and files with spaces or characters that need escaping can be put in quores.


##Changelog
* v1.0 Initial Release

##Author
Brian Mikolajczyk, brianm12@gmail.com
##Legal
###Licence
Please see file LICENCE.
###Copying
Please see file COPYING.
