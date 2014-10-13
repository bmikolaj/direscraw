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

def main(input=None):


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--version', action='version',
                        version='direscraw v1.24')
    parser.add_argument('-d', '--debug', action='store_true',
                         help=argparse.SUPPRESS)
    parser.add_argument('-b', '--blacklist', nargs='+',
        help='Add arguments separated by spaces to omit\
              filenames/directories')
    parser.add_argument('-n', '--nosum', action='store_true',
        help='No error percentage and runtime summary in subdirectories')
    parser.add_argument('-r', '--resume', action='store_true',
        help='Resumes a previously-interrupted direscraw session skipping\
              already recovered directories')

    main(**vars(parser.parse_args()))
