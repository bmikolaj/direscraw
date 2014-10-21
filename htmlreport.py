#!/usr/bin/env python
#HTML Report Generator, htmlreport v1.0
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
import os.path
import re
import wolframalpha

def main(input=None):
    client = wolframalpha.Client('K75WLW-XHVWW963YY')
    input = os.path.abspath(input)
    file = open(input, 'r')
    lines = file.readlines()
    file.close()
#Time summation
    timelist = []
    for i, line in enumerate(lines):
        if not line.startswith('/') and not i == 0 and not\
               line.endswith(';\n') and not line.endswith('RunTime\n') and not\
               line.startswith('\n'):
            timelist.append(re.split('%', line)[1].strip())

    entry = "'{}'".format('+'.join(map(str, timelist)))
    print(entry)
    out = client.query(entry, '*C.s-_*Unit-')
    for pod in out.pods:
        print(pod.text)

    print(out.pods[1].text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('--version', action='version',
                        version='htmlreport v1.0')

    main(**vars(parser.parse_args()))
