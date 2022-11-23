#!/usr/bin/env python3

import argparse
import os
import sys

from pathlib import Path
from pdf2image import convert_from_path
from PIL import Image
from tempfile import mkdtemp

argparser = argparse.ArgumentParser()
argparser.add_argument("--input", "-i", help="input file or directory (required)")
argparser.add_argument("--output", "-o", help="output directory")
argparser.add_argument("--format", "-f", help="output format")
argparser.add_argument("--lossless", "-l", help="lossless conversion", action="store_true")
argparser.add_argument("--prefix", "-p", help="prefix for output file(s)")
argparser.add_argument("--singlepage", "-s", help="get only the first page from input file(s)", action="store_true")
argparser.add_argument("--width", "-w", help="output width")

args = argparser.parse_args()

if not args.input:
    sys.exit("Input file or directory is required!")

multiple    = os.path.isdir(args.input)
i           = args.input
o           = args.output if args.output else (i if multiple else os.path.dirname(i))
fmt         = args.format.upper() if args.format else "JPEG"
ext         = fmt.lower() if fmt != 'JPEG' else 'jpg'
tmp_dir     = mkdtemp()
count       = 0
current     = 0
page_counts = []

def convert(i, o):
    f = os.path.basename(i)

    if(args.width):
        pages = convert_from_path(i, output_folder = tmp_dir, single_file = args.singlepage, size = (args.width, None))
    else:
        pages = convert_from_path(i, output_folder = tmp_dir, single_file = args.singlepage)

    if multiple:
        o = os.path.join(o, f.replace(".pdf", ""))
        Path(o).mkdir(parents = True, exist_ok = True)

    page_count = len(pages)
    j = 0
    k = 1

    if multiple:
        for a in range(current, count):
            page_counts[a] = page_count

        page_count = sum(page_counts)

        if current > 0:
            for a in range(0, current):
                j += page_counts[a]

    for page in pages:
        if args.singlepage:
            page.save(os.path.join(o, f.replace("pdf", ext)), format = fmt, lossless = args.lossless)
        else:
            page.save(os.path.join(o, (args.prefix if args.prefix else "") + str(k) + "." + ext), format = fmt, lossless = args.lossless)

        print("\033[F" + "\033[K" + str(round((j + k) / page_count * 100)) + "%")

        k += 1

print("0%")

if multiple:
    for root, dirs, files in os.walk(i):
        for f in files:
            if f.endswith(".pdf"):
                count += 1
                page_counts.append(0)

    for root, dirs, files in os.walk(i):
        for f in files:
            if f.endswith(".pdf"):
                convert(os.path.join(i, f), o)
                current += 1

else:
    convert(i, o)

print("\033[F" + "\033[K" + "Done")
