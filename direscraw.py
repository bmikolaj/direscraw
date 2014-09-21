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

    blacklist = set(["drclog","fulldrclog","error_summary"
    ,"full_error_summary"])
    with open(os.path.join(output_dir, 'fulldrclog'), 'w') as fulldrclog:
        for current_dir, _, unfilenames in os.walk(input_dir):
            filenames = sorted(unfilenames)
            relative_dir = os.path.relpath(current_dir, input_dir)
            #print relative_dir
            _, top_input_dir = os.path.split(os.path.abspath(input_dir))
            #print top_input_dir
            #current_out_dir = os.path.join(output_dir, relative_dir)
            current_out_dir = os.path.join(output_dir, top_input_dir, relative_dir)
            #print current_out_dir
            try:
                os.makedirs(current_out_dir)
            except OSError:
                pass

            with open(os.path.join(current_out_dir, 'drclog'), 'w+') as drclog:
                for filename in filenames:
                #for filename in [f for f in filenames if f not in blacklist]:
                    drclog.write('{}\n'.format(filename))
                    drclog.flush()
                    in_file_path = os.path.join(current_dir, filename)
                    out_file_path = os.path.join(current_out_dir, filename)
                    print in_file_path
                    subprocess.call(["ddrescue", in_file_path, out_file_path],
                                    stdout=drclog)
                drclog.seek(0)
                for line in drclog:
                    fulldrclog.write(line)
            
            with open(os.path.join(current_out_dir, 'error_summary'),
            'w') as error_summary:
                subprocess.call(['errcalc', os.path.join(current_out_dir, 'drclog')],
                                stdout=error_summary)
    
    with open(os.path.join(output_dir, 'full_error_summary'),
    'w') as full_error_summary:
        subprocess.call(['errcalc', os.path.join(output_dir, 'fulldrclog')],
                        stdout=full_error_summary)
    #shutil.move(os.path.join(output_dir, 'error_summary'),
    #            os.path.join(output_dir, 'full_error_summary'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dir')
    parser.add_argument('output_dir')

    main(**vars(parser.parse_args()))
