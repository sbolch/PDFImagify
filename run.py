#!/usr/bin/env python

import argparse
import os
import sys
import tempfile

from pdf2image import convert_from_path
from PIL import Image

argparser = argparse.ArgumentParser()
argparser.add_argument("--input", help="input file or directory")
argparser.add_argument("--output", help="output directory")
argparser.add_argument("--format", help="output format")
argparser.add_argument("--lossless", "-l", help="lossless conversion", action="store_true")
argparser.add_argument("--multiple", "-m", help="convert all files from input directory", action="store_true")
argparser.add_argument("--prefix", help="prefix for output file(s)")
argparser.add_argument("--singlepage", "-s", help="get only the first page from input file(s)", action="store_true")
argparser.add_argument("--width", help="output width")

args = argparser.parse_args()

if not args.input:
    sys.exit("Input file or directory is required!")

_input     = args.input
_output    = args.output if args.output else (_input if os.path.isdir(_input) else os.path.dirname(_input))
_format    = args.format.upper() if args.format else "JPEG"
_extension = _format.lower() if _format != 'JPEG' else 'jpg'

tmp_dir = tempfile.mkdtemp()

def convert(i, o):
    f = os.path.basename(i)

    if(args.width):
        pages = convert_from_path(i, output_folder = tmp_dir, single_file = args.singlepage, size = (args.width, None))
    else:
        pages = convert_from_path(i, output_folder = tmp_dir, single_file = args.singlepage)

    if args.multiple:
        o = os.path.join(o, f.replace(".pdf", ""))
        os.mkdir(o)

    j = 1
    for page in pages:
        if args.singlepage:
            page.save(os.path.join(o, f.replace("pdf", _extension)), format = _format, lossless = args.lossless)
        else:
            page.save(os.path.join(o, (args.prefix if args.prefix else "") + str(j) + "." + _extension), format = _format, lossless = args.lossless)

        j += 1

if args.multiple:
    count = 0
    for root, dirs, files in os.walk(_input):
        for f in files:
            count += 1

    i = 0
    print("0%")
    for root, dirs, files in os.walk(_input):
        for f in files:
            convert(os.path.join(_input, f), _output)

            print("\033[F" + "\033[K" + str(round(i / count * 100)) + "%")
            i += 1

    print("\033[F" + "\033[K")

else:
    convert(_input, _output)

print("Done")
