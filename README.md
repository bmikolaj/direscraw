#Directory Rescue Crawler
v1.24

#####Errcalc v1.0

##Description

Directory Rescue Crawler uses `ddrescue` to recover full directories from one location to another. This program also prints an error and runtime summary in each subdirectory copied and a full summary in the root directory via the included `errcalc` program. 

##Dependencies
Directory Rescue Crawler was designed for Linux and uses the following programs;

* Bash
* Python 2.7+
* GNU ddrescue (installed via setup.sh)
* GNU Units (installed via setup.sh)
* g++ (for installation; installed via setup.sh)
* Lzip (for installation; installed via setup.sh)
* Gunzip (for installation)
* Tar (for installation)


##Install
* Clone git archive via the following command; 
  
  `git clone https://github.com/p014k/direscraw.git direscraw`
* Change directories via `cd direscraw`
* Run the following command to install;
  
  `sudo ./setup.sh install`

This will install two programs: Directory Rescue Crawler (`direscraw`) and the Error Percentage and Runtime Calculation Summary (`errcalc`) to /usr/local/bin.

##Usage
Run from the command line;

`direscraw [-h] <input_directory> <output_directory> [-r] [-n] [-b] BLACKLIST`

####Required parameters
`<input_directory>` and `<output_directory>` are required.

####Optional parameters
`-h` for help

`--version` will print the version of `direscraw` and exit.

`-n`, `--nosum` will run the program without `errcalc` thus creating no Error Percentage and Runtime Calculation files.

`-b BLACKLIST`, `--blacklist BLACKLIST` specifies a list of files and/or directories (separated by a space) to omit from rescuing (case-sensitive). Wildcards are accepted.

`-r`, `--resume` will resume a previously-interrupted session of `direscraw` skipping already rescued files. 

###Example 
`user@computer:$ direscraw /media/Drive1/ /media/Drive2/Backup/ -b *.mp3 'Pictures Of Me'` (This will omit all mp3 files and a directory called Pictures Of Me). 

Note: Directories and files with characters that need escaping can be put in quotes. Files and directories are case-sensitive. Wildcards are accepted.

##Uninstall
* Run the following command to uninstall;
  
  `sudo ./setup.sh uninstall`

##Changelog
* v1.24 (12 October 2014)

  Added g++ to setup.sh

  Added --version support

* v1.23 (11 October 2014)

  Removed regex in favor of pythonic solution to hidden directories.

* v1.22 (09 October 2014)

  Fixed hidden directory omission error.

* v1.21 (08 October 2014)

  Fixed file-only wildcard bug in blacklist

* v1.2 (08 October 2014)

  Added resume support option, `-r`

  Added wildcard ability to blacklist

  Added timestamp to error_summary and full_error_summary

* v1.16 (05 October 2014)

  Now prints directory in error_summary and full_error_summary

* v1.15 (04 October 2014)

  Combined install and uninstall into setup.sh

* v1.1 (03 October 2014)

  Added suppression of Error Percentage and Runtime Calculation option, `-n`

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
