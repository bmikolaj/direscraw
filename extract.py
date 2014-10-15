#!/usr/bin/env python

################################################################################
#Authors: Brian Mikolajczyk and Gary Foreman
#Last Modified: October 15, 2014
#Reads in file given as command argument. Searches for each instance of string
#"Finished", and prints preceding three lines.
################################################################################

import argparse
import os.path
import re

def main(input=None):
    with open(os.path.abspath(input), 'r') as infile:
        lines = infile.readlines()


#Clip input to match number of files
    first_string = 'rescued'       
    end_string = 'Finished'
    newlines = []
    n_occurances = 0
    for i, line in enumerate(lines):
        if re.search(end_string, line):
            n_occurances = n_occurances + 1
            for j in range(3):
                current_line = lines[i - 3 + j]
                if re.search(first_string, current_line):
                    current_line = (first_string +
                                    re.split(first_string, current_line)[1])
                    
                newlines.append(current_line.strip())

    #print(newlines)
#Split into calculable variables
    rescued = []
    errsize = []
    runtime = []
    for line in newlines:
        if re.search(first_string, line):
            delim = re.split(': |, ', line)
            rescued.append(delim[1].strip().replace(' ',''))
            errsize.append(delim[3].strip().replace(' ',''))
        if re.search('opos', line):
            delim = re.split(': |, ', line)
            runtime.append(delim[3].strip().replace(' ',''))
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='errcalc v2.0')

    main(**vars(parser.parse_args()))
