#!/usr/bin/env python

################################################################################
#Authors: Brian Mikolajczyk and Gary Foreman
#Last Modified: October 14, 2014
#Reads in file given as command argument. Searches for each instance of string
#"Finished", and prints preceeding three lines.
################################################################################

from __future__ import print_function

import argparse
import os.path
import re


PRECEDING_LINES = 3
FINISHED_REGEX = 'Finished'
SPLIT_REGEX = 'rescued'
OUTPUT_FILE = 'drclog2'


def main(input=None):
    with open(input) as infile:
        lines = infile.readlines()

    with open(OUTPUT_FILE, 'w') as outfile:
        for i, line in enumerate(lines):
            if re.search(FINISHED_REGEX, line):
                for j in xrange(PRECEDING_LINES):
                    current_line = lines[i - PRECEDING_LINES + j]
                    if re.search(SPLIT_REGEX, current_line):
                        current_line = (SPLIT_REGEX + 
                                        re.split(SPLIT_REGEX, current_line)[1])
                    print(current_line.strip())
                    outfile.write(current_line.strip())
                print('\n')
                outfile.write('\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='errcalc v2.0')

    main(**vars(parser.parse_args()))
