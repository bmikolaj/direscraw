#!/usr/bin/env python
#Directory Rescue Crawler, direscraw v1.1
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

import os.path
import argparse
import subprocess
from pipes import quote

def main(input_dir=None, output_dir=None, blacklist=None, nosum=False):
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    if not nosum:
        oblist = set(["drclog","fulldrclog","error_summary"
        ,"full_error_summary"])
    else:
        oblist = set(["drclog","fulldrclog"])

    if blacklist is None:
        blacklist = oblist
    else:
        blacklist = set(blacklist) | oblist
    
    _, top_input_dir = os.path.split(os.path.abspath(input_dir))
    with open(os.path.join(output_dir, 'fulldrclog'), 'w') as fulldrclog:
        for current_dir, dirnames, unfilenames in os.walk(input_dir):
            dirnames[:] = set(dirnames) - blacklist
            filenames = sorted(unfilenames)
            relative_dir = os.path.relpath(current_dir, input_dir)
            current_out_dir = os.path.join(output_dir, top_input_dir, 
            relative_dir)
            try:
                os.makedirs(current_out_dir)
            except OSError:
                pass

            with open(os.path.join(current_out_dir, 'drclog'), 'w+') as drclog:
                for filename in [f for f in filenames if f not in blacklist]:
                    drclog.write('{}\n'.format(filename))
                    drclog.flush()
                    in_file_path = os.path.join(current_dir, filename)
                    out_file_path = os.path.join(current_out_dir, filename)
                    files = in_file_path, out_file_path
                    print('\n' + in_file_path)
                    subprocess.call("ddrescue {} |  tee -a {}"
                        .format(' '.join(map(quote, files)),
                        quote(os.path.join(current_out_dir, 'drclog'))), shell=True)
                drclog.seek(0)
                for line in drclog:
                    fulldrclog.write(line)

            if not nosum:
                with open(os.path.join(current_out_dir, 'error_summary'),
                'w') as error_summary:
                    error_summary.write('File Error% RunTime' + '\n')
                    error_summary.flush()
                    subprocess.call(['errcalc', os.path.join(current_out_dir,
                                    'drclog')], stdout=error_summary)

            os.remove(os.path.join(current_out_dir, 'drclog'))

    if not nosum:
        with open(os.path.join(output_dir, 'full_error_summary'),
        'w') as full_error_summary:
            full_error_summary.write('File Error% RunTime' + '\n')
            full_error_summary.flush()
            subprocess.call(['errcalc', os.path.join(output_dir, 'fulldrclog')],
                            stdout=full_error_summary)

    os.remove(os.path.join(output_dir, 'fulldrclog'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('-b', '--blacklist', nargs='+',
        help="Add arguements separated by spaces to omit filenames/directories")
    parser.add_argument('-n', '--nosum', action='store_true',
        help="No error percentage and runtime summary in subdirectories")

    main(**vars(parser.parse_args()))
