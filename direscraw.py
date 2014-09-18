#!/usr/bin/env python

import shutil
import os.path
import argparse
import subprocess

def main(input_dir=None, output_dir=None):
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    with open(os.path.join(output_dir, 'fulldrclog'), 'w') as fulldrclog:
        # Traverses the entire input directory tree.
        # Does *not* follow symlinks and following them could cause loops.
        for current_dir, _, filenames in os.walk(input_dir):
            relative_dir = os.path.relpath(current_dir, input_dir)
            current_out_dir = os.path.join(output_dir, relative_dir)
            try:
                os.mkdir(current_out_dir)
            except OSError:
                # Raised if the dir exists; handle appropriately or do nothing.
                pass

            with open(os.path.join(current_out_dir, 'drclog'), 'w+') as drclog:
                for filename in filenames:
                    # Might want to consider desired behavior if filename is
                    # drclog or fulldrclog...
                    drclog.write('{}\n'.format(filename))
                    drclog.flush()
                    in_file_path = os.path.join(current_dir, filename)
                    out_file_path = os.path.join(current_out_dir, filename)
                    subprocess.call(['ddrescue', in_file_path, out_file_path],
                                    stdout=drclog)
                # It's annoying to write to both files from subprocess, so we
                # copy the contents of drclog into fulldrclog when we're done.
                drclog.seek(0)
                for line in drclog:
                    fulldrclog.write(line)
    subprocess.call(['errcalc', os.path.join(output_dir, 'fulldrclog')])
    shutil.move(os.path.join(output_dir, 'error_summary'),
                os.path.join(output_dir, 'full_error_summary'))

# This is a pretty common Python idiom which lets your code be imported as
# a module or run standalone from the command line.
if __name__ == '__main__':
    # I think this requires Python 2.7+
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')

    # This is kind of ugly, but whatever; I don't like passing the Namespace.
    main(**vars(parser.parse_args()))
