#!/usr/bin/env python
#Error Percentage and Runtime Calculation Summary, errcalc v2.0
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
from itertools import ifilter
import os.path
import re
import subprocess

def main(input=None):
    f = open(os.path.abspath(input),'r')
    file = f.readlines()
    f.close()
    #a_string = re.compile(r'\x1b\[A')
    #b_string = re.compile(r'\rCopying\ non-tried\ blocks...\ Pass\ 1\ \(forwards\)\r')
    #file = a_string.sub('', file)
    #file = b_string.sub('', file)
    num = re.findall(r'Finished', file, re.X).groups()
    file = ''.join(re.search(r'(Press.*?)\r(Finished.*)', file, re.DOTALL).groups())
    #file = ''.join(re.search(r'(rescued:.*?)\r(Finished.*)', file, re.DOTALL).groups())
    print(num)
    omit = ['GNU', 'Finished', 'Pressed']
    #open('drclog2', 'w').write(file)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='errcalc v2.0')

    main(**vars(parser.parse_args()))
