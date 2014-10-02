#!/usr/bin/env python
#Directory Rescue Crawler, direscraw v1.0
#Written by Brian Mikolajczyk, brianm12@gmail.com

import os.path
import argparse
import subprocess
from pipes import quote

def main(input_dir=None, output_dir=None, blacklist=None):
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    oblist = set(["drclog","fulldrclog","error_summary"
    ,"full_error_summary"])
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
                        os.path.join(current_out_dir, 'drclog')), shell=True)
                drclog.seek(0)
                for line in drclog:
                    fulldrclog.write(line)
            
            with open(os.path.join(current_out_dir, 'error_summary'),
            'w') as error_summary:
                error_summary.write('File Error% RunTime' + '\n')
                error_summary.flush()
                subprocess.call(['errcalc', os.path.join(current_out_dir,
                                'drclog')], stdout=error_summary)
                os.remove(os.path.join(current_out_dir, 'drclog'))

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

    main(**vars(parser.parse_args()))
