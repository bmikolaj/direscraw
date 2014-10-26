#!/usr/bin/env python
#Directory Rescue Crawler, direscraw v2.0
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
import fnmatch
import os.path
from pipes import quote
import subprocess
import time

def main(input_dir=None, output_dir=None, blacklist=None, nosum=False,
                                           resume=False, debug=False):
    if debug:
        print("Debugging mode: drclog retention enabled." + '\n')

    input_dir = os.path.abspath(input_dir)
    output_dir = os.path.abspath(output_dir)
    try:
        os.mkdir(output_dir)
    except OSError:
        pass
#Handling of blacklist
    oblist = set(['drclog', 'error_summary', 'full_error_summary'])
    if blacklist is None:
        blwild = False
        blacklist = oblist
    else:
        blwild = True
        blacklist = set(blacklist) | oblist

    tfmt = '%Y-%m-%d %H:%M:%S'
    top_input_dir = os.path.split(input_dir)[1]
    fullskipset = set([])
    if os.path.isfile(os.path.join(output_dir, 'full_error_summary')) and not\
                                                                       resume:
        os.remove(os.path.join(output_dir, 'full_error_summary'))
    
    with open(os.path.join(output_dir, 'full_error_summary'),
                           'w+') as full_error_summary:
        if not nosum:
            full_error_summary.write('File Error% RunTime' + '\n')
#Starting os.walk for loop
        for current_dir, dirnames, unfilenames in os.walk(input_dir):
        #Check for wildcards in blacklist
            if blwild:
                infiles = set([f for f in os.listdir(
                                     current_dir)]) - blacklist
                wildlist = []
                for el in blacklist:
                    wildlist = wildlist + fnmatch.filter(infiles, el)
                
                blacklist = blacklist | set(wildlist)

            dirnames[:] = set(dirnames) - blacklist
            filenames = sorted(unfilenames)
            relative_dir = os.path.relpath(current_dir, input_dir)
            current_out_dir = os.path.join(output_dir,
                              top_input_dir, relative_dir)
            if os.path.split(current_out_dir)[1] == '.':
                current_out_dir = os.path.split(current_out_dir)[0]

            try:
                os.makedirs(current_out_dir)
            except OSError:
                pass

            if resume:
                outfiles = list(set([f for f in os.listdir(current_out_dir)
                                      if os.path.isfile(os.path.join(
                                      current_out_dir, f))]) - blacklist)
                if len(filenames) == len(outfiles) and not\
                     os.path.isfile(os.path.join(current_out_dir, 'copylog')):
                    continue

                try:
                    sindex = filenames.index(outfiles[-1])
                except (IndexError, ValueError):
                    sindex = 0
            else:
                sindex = 0
            
            skipset = set([])
            with open(os.path.join(current_out_dir, 'drclog'),
                      'w+') as drclog, open(os.path.join(current_out_dir,
                                                         'copylog'), 'w'):
            #Start directory loop
                for filename in [f for f in filenames[sindex:]
                                         if f not in blacklist]:
                    in_file_path = os.path.join(current_dir, filename)
                    out_file_path = os.path.join(current_out_dir, filename)
                    files = in_file_path, out_file_path
                    drclog.write('{}\n'.format(filename))
                    drclog.flush()
                    print('\n' + in_file_path)
                    try:
                        subprocess.call('ddrescue {} |  tee -a {}'
                            .format(' '.join(map(quote, files)),
                            quote(os.path.join(current_out_dir, 'drclog'))),
                                               shell=True)
                    except KeyboardInterrupt:
                        skipset.add(in_file_path)
                        fullskipset.add(in_file_path)
                        print('\n' + in_file_path + ' has been skipped')
                        continue

                drclog.seek(0)
            #Creating error report
                if not nosum:
                    with open(os.path.join(current_out_dir, 'error_summary'),
                                           'w') as error_summary:
                        error_summary.write(time.strftime(tfmt) + '\n')
                        error_summary.write(current_out_dir + '\n')
                        if len(skipset) > 0:
                            error_summary.write('\n' + 'Files Skipped: '\
                                            + str(len(skipset)) + ';' + '\n')
                            for skipel in skipset:
                                error_summary.write(skipel + '\n')

                            error_summary.write('\n')

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
                        subprocess.call(['htmlrepgen',
                              os.path.join(current_out_dir, 'error_summary')])

            if not debug:
                os.remove(os.path.join(current_out_dir, 'drclog'))
            
            os.remove(os.path.join(current_out_dir, 'copylog'))
#Creating full error report    
    if not nosum:
        FES = open(os.path.join(output_dir, 'full_error_summary'))
        FES_lines = FES.readlines()
        FES.close()
        with open(os.path.join(output_dir, 'full_error_summary'),
                               'w') as full_error_summary:
            full_error_summary.write(time.strftime(tfmt) + '\n')
            if len(fullskipset) > 0:
                full_error_summary.write('\n' + 'Files Skipped: '\
                                         + str(len(fullskipset)) + ';' + '\n')
                for skipel in fullskipset:
                    full_error_summary.write(skipel + '\n')
            
            full_error_summary.write('\n')
            
            full_error_summary.flush()
            for lines in FES_lines:
                full_error_summary.write(lines)

        subprocess.call(['htmlrepgen', '-f',
                        os.path.join(output_dir, 'full_error_summary')])
    else:
        os.remove(os.path.join(output_dir, 'full_error_summary'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')
    parser.add_argument('--version', action='version',
                        version='direscraw v2.0; errcalc v2.2; htmlrepgen v1.0')
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
