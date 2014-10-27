#!/usr/bin/env python

import argparse
import pdfkit
import os.path

def main(input=None):
    input = os.path.abspath(input)
    input2 = input.rsplit('.', 1)[0] + '2.' + input.rsplit('.', 1)[1]
    output_dir = os.path.split(input)[0]
    output = input.rsplit('.', 1)[0] + '.pdf'
    options = {
        'quiet': '',
        'image-dpi': '1000',
        'image-quality': '100'
        }
    pdfkit.from_file(input, output, options=options)
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')

    main(**vars(parser.parse_args()))
