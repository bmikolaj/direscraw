#Directory Rescue Crawler
v1.3

#####Errcalc v1.0

##Description

Directory Rescue Crawler uses `ddrescue` to recover full directories from one location to another. This program also prints an error and runtime summary in each subdirectory copied and a full summary in the root directory via the included `errcalc` program.

##Dependencies
Directory Rescue Crawler was designed for Linux and uses the following programs;

* Bash
* Python 2.7+
* Gunzip
* Tar
* Lzip (installed via setup.sh)
* GNU ddrescue (installed via setup.sh)
* GNU Units (installed via setup.sh)

##Install
* Clone git archive via the following command; 
  
  `git clone https://github.com/p014k/direscraw.git direscraw`
* Change directories via `cd direscraw`
* Run the following command to install;
  
  `sudo ./setup.sh install`

This will install two programs: Directory Rescue Crawler (`direscraw`) and the Error Percentage and Runtime Calculation Summary (`errcalc`) to /usr/local/bin.

##Usage
Run from the command line;

`direscraw [-h] <input_directory> <output_directory> [-n] [-b] BLACKLIST`

####Required parameters
`<input_directory>` and `<output_directory>` are required.

####Optional parameters
`-h` for help

`-n`,`--nosum` will run the program without `errcalc` thus creating no Error Percentage and Runtime Calculation files.

`-b BLACKLIST`, `--blacklist BLACKLIST` specifies a list of files and/or directories separated by a space to omit from rescuing (case-sensitive). 

###Example 
`use@computer:$ direscraw /media/Drive1/ /media/Drive2/Backup/ -b .mp3 'Pictures Of Me'` (This will omit all mp3 files and a directory called Pictures Of Me). 

Note: Directories and files with spaces or characters that need escaping can be put in quores.

##Uninstall
* Run the following command to uninstall;
  
  `sudo ./setup.sh uninstall`

##Changelog
* v1.3 (05 October 2014)

  Now prints directory in error_summary and full_error_summary 

* v1.2 (04 October 2014)

  Combined install and uninstall into setup.sh

* v1.1 (03 October 2014)

  Added supression of Error Percentage and Runtime Calculation option, `-n`

* v1.0 (03 October 2014)

  Initial Release

##Development Notes
Tested with the following program versions;

* Bash v4.3.11(1)-release (i686-pc-linux-gnu)
* Python 2.7.6
* GNU ddrescue 1.18.1
* GNU Units v2.02

##Author
[Brian Mikolajczyk](https://github.com/p014k), brianm12@gmail.com

##Legal
Copyright (c) 2014, Brian Mikolajczyk, brianm12@gmail.com

###Licence
Please see file LICENCE.

###Copying
Please see file COPYING.
