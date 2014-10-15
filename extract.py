#!/usr/bin/env python

################################################################################
#Authors: Brian Mikolajczyk and Gary Foreman
#Last Modified: October 15, 2014
#Reads in file given as command argument. Searches for each instance of string
#"Finished", and prints preceding three lines.
################################################################################

import argparse
import bitmath
import os.path
import re

def main(input=None):
    with open(os.path.abspath(input), 'r') as infile:
        lines = infile.readlines()


#Clip input to match number of files
    first_string = 'rescued'       
    end_string = 'Finished'
    newlines = []
    n_files = 0
    for i, line in enumerate(lines):
        if re.search(end_string, line):
            n_files = n_files + 1
            for j in xrange(3):
                current_line = lines[i - 3 + j]
                if re.search(first_string, current_line):
                    current_line = (first_string +
                                    re.split(first_string, current_line)[1])
                    
                newlines.append(current_line.strip())

    files = [x.replace('\n','') for x in lines[0:n_files]]

#Split into calculable variables
    rescued_num = []
    rescued_unit = []
    errsize_num = []
    errsize_unit = []
    runtime = []
    for line in newlines:
        if re.search(first_string, line):
            delim = re.split(': |, ', line)
            rescued_num.append(re.split(' ', delim[1].strip())[0])
            rescued_unit.append(re.split(' ', delim[1].strip())[1])
            errsize_num.append(re.split(' ', delim[3].strip())[0])
            errsize_unit.append(re.split(' ', delim[3].strip())[1])
        if re.search('opos', line):
            delim = re.split(': |, ', line)
            runtime.append(delim[3].strip().replace(' ',''))

#Calculations
    for i in xrange(n_files):
        #Conversion to bitmath format: rescued
        if rescued_unit[i] == 'B':
            rescued_num[i] = 'bitmath.Byte(' + rescued_num[i] + ')'
            
        if rescued_unit[i] == 'kB':
            rescued_num[i] = 'bitmath.KiB(' + rescued_num[i] + ')'
            
        if rescued_unit[i] == 'Mb': #Verify via ddrescue
            rescued_num[i] = 'bitmath.MiB(' + rescued_num[i] + ')'
            
        if rescued_unit[i] == 'Gb': #Verify via ddrescue
            rescued_num[i] = 'bitmath.GiB(' + rescued_num[i] + ')'
            
        #Conversion to bitmath format: errsize
        if errsize_unit[i] == 'B':
            errsize_num[i] = 'bitmath.Byte(' + errsize_num[i] + ')'
            
        if errsize_unit[i] == 'kB':
            errsize_num[i] = 'bitmath.KiB(' + errsize_num[i] + ')'
            
        if errsize_unit[i] == 'Mb': #Verify via ddrescue
            errsize_num[i] = 'bitmath.MiB(' + errsize_num[i] + ')'
            
        if errsize_unit[i] == 'Gb': #Verify via ddrescue
            errsize_num[i] = 'bitmath.GiB(' + errsize_num[i] + ')'
        
        total_size = rescued_num[i] + errsize_num[i]
        print(total_size)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='errcalc v2.0')

    main(**vars(parser.parse_args()))
