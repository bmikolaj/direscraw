#!/usr/bin/env python
#Error Report Generator v1.0
#Copyright (c) 2014 by Brian Mikolajczyk, brianm12@gmail.com

#For generating error reports from 'drclog' files in copied directory

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

import argparse
import os.path
import subprocess
import time

def main(input_dir=None, debug=False):
    input_dir = os.path.abspath(input_dir)
    tfmt = '%Y-%m-%d %H:%M:%S'
    with open(os.path.join(input_dir, 'full_error_summary'),
                           'w+') as full_error_summary:
        full_error_summary.write('File Error% RunTime' + '\n')
#Starting os.walk for loop
        for current_dir, _, _ in os.walk(input_dir):
            relative_dir = os.path.relpath(current_dir, input_dir)
            current_out_dir = os.path.join(input_dir, relative_dir)
            if os.path.split(current_out_dir)[1] == '.':
                current_out_dir = os.path.split(current_out_dir)[0]

            if not os.path.isfile(os.path.join(current_out_dir, 'drclog')):
                continue

            #Creating error report
            with open(os.path.join(current_out_dir, 'error_summary'),
                                   'w') as error_summary:
                error_summary.write(time.strftime(tfmt) + '\n')
                error_summary.write(current_out_dir + '\n')
                error_summary.write('File Error% RunTime' + '\n')
                error_summary.flush()
                full_error_summary.write(current_out_dir + '\n')
                full_error_summary.flush()
                subprocess.call(['errcalc',
                                os.path.join(current_out_dir,
                                'drclog')], stdout=error_summary)
                subprocess.call(['errcalc',
                                os.path.join(current_out_dir,
                                'drclog')], stdout=full_error_summary)

            if not debug:
                os.remove(os.path.join(current_out_dir, 'drclog'))
            
#Creating full error report    
    FES = open(os.path.join(input_dir, 'full_error_summary'))
    FES_lines = FES.readlines()
    FES.close()
    with open(os.path.join(input_dir, 'full_error_summary'),
                           'w') as full_error_summary:
        full_error_summary.write(time.strftime(tfmt) + '\n')
        full_error_summary.write('\n')
        full_error_summary.flush()
        for lines in FES_lines:
            full_error_summary.write(lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('--version', action='version', 
                        version='genreports v1.0')
    parser.add_argument('-d', '--debug', action='store_true',
                        help=argparse.SUPPRESS)

    main(**vars(parser.parse_args()))
