#!/usr/bin/env python
#Error Percentage and Runtime Calculation Summary, errcalc v2.2
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


import argparse
import bitmath
import os.path
import re
import time

def main(input=None, standalone=False):
    tfmt = '%Y-%m-%d %H:%M:%S'
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
    runtime_unit = []
    for line in newlines:
        if re.search(first_string, line):
            delim = re.split(': |, ', line)
            rescued_num.append(re.split(' ', delim[1].strip())[0])
            rescued_unit.append(re.split(' ', delim[1].strip())[1])
            errsize_num.append(re.split(' ', delim[3].strip())[0])
            errsize_unit.append(re.split(' ', delim[3].strip())[1])
        elif re.search('opos', line):
            delim = re.split(': |, ', line)
            runtime.append(re.split(' ', delim[3].strip())[0])
            runtime_unit.append(re.split(' ', delim[3].strip())[1])

#Calculations
    errper = []
    for i in xrange(n_files):
        #Conversion of runtime_unit to string
        if runtime_unit[i] == 'm':
            if runtime[i] == '1':
                runtime_unit[i] = 'min'
            else:
                runtime_unit[i] = 'mins'
        
        elif runtime_unit[i] == 'h':
            if runtime[i] == '1':
                runtime_unit[i] = 'hr'
            else:
                runtime_unit[i] = 'hrs'
        
        elif runtime_unit[i] == 'd':
            if runtime[i] == '1':
                runtime_unit[i] = 'day'
            else:
                runtime_unit[i] = 'days'
            
        #Conversion to bitmath format: rescued
        if rescued_unit[i] == 'B':
            rescued_num[i] = bitmath.Byte(float(rescued_num[i]))
            
        elif rescued_unit[i] == 'kB':
            rescued_num[i] = bitmath.KiB(float(rescued_num[i]))
            
        elif rescued_unit[i] == 'MB':
            rescued_num[i] = bitmath.MiB(float(rescued_num[i]))
            
        elif rescued_unit[i] == 'Gb': #Verify via ddrescue
            rescued_num[i] = bitmath.GiB(float(rescued_num[i]))
            
        #Conversion to bitmath format: errsize
        if errsize_unit[i] == 'B':
            errsize_num[i] = bitmath.Byte(float(errsize_num[i]))
            
        elif errsize_unit[i] == 'kB':
            errsize_num[i] = bitmath.KiB(float(errsize_num[i]))
            
        elif errsize_unit[i] == 'MB':
            errsize_num[i] = bitmath.MiB(float(errsize_num[i]))
            
        elif errsize_unit[i] == 'Gb': #Verify via ddrescue
            errsize_num[i] = bitmath.GiB(float(errsize_num[i]))
        
        try:
            errper.append((errsize_num[i] / (rescued_num[i]
                          + errsize_num[i])) * 100)
        except ZeroDivisionError:
            errper.append(0)
        
    for i, line in enumerate(errper):
        errper[i] = format(line, '.2f').rstrip('0').rstrip('.') + '%'

#Concaterate lists
    if standalone:
        output_dir = os.path.split(os.path.abspath(input))[0]
        output = open(os.path.join(output_dir, 'error_summary'), 'w')
        output.write(time.strftime(tfmt) + '\n')
        output.write(output_dir + '\n')
        output.write('File Error% RunTime' + '\n')
        output.flush()

    for i in xrange(n_files):
        if standalone:
            output.write(files[i] + ' ' + errper[i] + ' ' +
                         '{} {}'.format(runtime[i], runtime_unit[i]) + '\n')
            output.flush()

        else:
            print(files[i] + ' ' + errper[i] + ' ' +
                  '{} {}'.format(runtime[i], runtime_unit[i]))

    if standalone:
        output.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('-s', '--standalone', action='store_true',
                        help=argparse.SUPPRESS)
    parser.add_argument('--version', action='version',
                        version='errcalc v2.2')

    main(**vars(parser.parse_args()))
