#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from ProcessTile.process import *
    
def parse_tilefilespecs(tilefilespec, output = None, verbose = False):
    for tfs in parse_tilefilespec(tilefilespec, verbose = verbose):
        process_tilespec(tfs, outfile = output if (output is not None) else tfs.output, verbose = verbose)
    
def main():
    import argparse
    parser = argparse.ArgumentParser(description='Join Tilemaps')
    parser.add_argument('-i', '--input', dest='input', action='store',
                        default=None, help='input tile script.')
    parser.add_argument('-o', '--output', dest='output', action='store',
                        default=None, help='output tile file.')
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                        default=False, help='chatty or not.')
    
    args = parser.parse_args()
    parse_tilefilespecs(args.input, output=args.output, verbose=args.verbose)

if __name__ == "__main__":
    main()
    
