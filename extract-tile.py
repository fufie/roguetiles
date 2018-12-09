#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ProcessTile.process import *

def extract_tile(infile, tilenumber, outfile, xoffset = 0, yoffset = 0, verbose = False):
    tile = TileTransfer(infile, tilenumber, target_tile = 0, source_xoffset=xoffset, source_yoffset=yoffset)
    tilespec = TileFileSpecification(outfile, width=32, height=32, tiles=[tile])
    process_tilespec(tilespec, outfile, verbose = verbose)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Join Tilemaps')
    parser.add_argument('-i', '--input', dest='input', action='store',
                        default=None, help='input tile file.')
    parser.add_argument('-o', '--output', dest='output', action='store',
                        default=None, help='output tile file.')
    parser.add_argument('-t', '--tilenumber', dest='tilenumber', type=int,
                        default=0, help='number of tile to extract.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        default=False, help='chatty or not.')
    parser.add_argument('-x', '--xoffset', dest='xoffset', type=int,
                        default=0, help='xoffset.')
    parser.add_argument('-y', '--yoffset', dest='yoffset', type=int,
                        default=0, help='yoffset.')
    
    args = parser.parse_args()

    if args.input is None:
        print "Error. No input provided"
        sys.exit(-1)

    extract_tile(args.input, args.tilenumber, args.output, xoffset=args.xoffset, yoffset=args.yoffset, verbose = args.verbose)

if __name__ == "__main__":
    main()
    
