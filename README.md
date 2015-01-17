#Directory Rescue Crawler
v2.0

#####Errcalc v2.2
#####Htmlrepgen v1.0

##Description

Directory Rescue Crawler uses `ddrescue` to recover full directories from one location to another. `ddrescue` by itself can only recover individual files or full filesystems.

This program also prints an error and runtime summary in each subdirectory copied and a full summary in the top-most directory via the included `errcalc` program. This report is then fed into `htmlrepgen` to generate a full HTML report (`direscraw_HTMLReport.html`) in the top-most directory.

##Dependencies
Directory Rescue Crawler was designed for Linux and uses the following programs;

* Git
* Bash
* Python 2.7+
* GNU ddrescue (installed via setup.sh)
* Python `setuptools` (installed via setup.sh)
* Python module: `bitmath` (installed via setup.sh)
* Python module: `numpy` (installed via setup.sh)
* Python module: `plotly` (installed via setup.sh)
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

`-b BLACKLIST`, `--blacklist BLACKLIST` specifies a list of files and/or directories (separated by a space) to omit from rescuing (case-sensitive). Wildcards are accepted.

`-n`, `--nosum` will run the program without `errcalc` thus creating no Error Percentage and Runtime Calculation files.

`-r`, `--resume` will resume a previously-interrupted session of `direscraw` skipping already rescued files. 

###Example 
`user@computer:$ direscraw /media/Drive1/ /media/Drive2/Backup/ -b *.mp3 'Pictures Of Me'` (This will omit all mp3 files and a directory called Pictures Of Me). 

Note: Directories and files with characters that need escaping can be put in quotes. Files and directories are case-sensitive. Wildcards are accepted.

If `ddrescue` is running to long, or you want to manually skip a file while it's copying, `CTRL+C` will skip the file. A note of the skipped file is written to the error report of that directory and to the full error report in the root directory.

##Uninstall
* Run the following command to uninstall;
  
  `sudo ./setup.sh uninstall`

##Changelog
* v2.0

  Added HTML Report, `htmlrepgen`

  Updated `setup.sh`, `direscraw`, and `errcalc` to reflect changes

  Removed easy_install from setup.sh; now unnecessary. Changed `bitmath` module install to `pip`

* v1.43 (20 October 2014)

  Added setuptools to setup.sh

* v1.42 (19 October 2014)

  Added number of files skipped to error reporting

  Changed `bitmath` module install to `easy_install`

* v1.41 (18 October 2014)

  Added skip reporting to full_error_summary

  Stylized run time units reporting in error summary reports; `errcalc` v2.1

  Added `errcalc` to `--version`

* v1.4 (16 October 2014)

  Updated `direscraw` to reflect changes

  Rewrote `errcalc` in python; v2.0 ---Special thanks to [Gary Foreman](https://github.com/garyForeman) for all the help

  Removed GNU Units from setup.sh; now unnecessary. Added `bitmath` Python module to setup.sh


* v1.3 (13 October 2014)

  Added ability to skip a `ddrescue` instance.

  Added g++ to setup.sh

  Added drclog debugger (for development only)

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
* Python `bitmath` module v1.0.8
* Python `numpy` module v1.9.0
* Python `plotly` module v1.3.1
* GNU ddrescue 1.18.1

##Author
[Brian Mikolajczyk](https://github.com/bmikolaj), brianm12@gmail.com

##Legal
Copyright (c) 2014, Brian Mikolajczyk, brianm12@gmail.com

###Licence
Please see file LICENCE.

###Copying
Please see file COPYING.
