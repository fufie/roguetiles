#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import pprint
from PIL import Image

class TileTransfer:
    filename = None
    source_tile = 0
    target_tile = -1
    source_xoffset = 0
    source_yoffset = 0
    
    def __init__(self, filename, source_tile, target_tile = -1, source_xoffset = 0, source_yoffset = 0):
        self.filename = filename
        self.source_tile = source_tile
        self.target_tile = target_tile
        self.source_xoffset = source_xoffset
        self.source_yoffset = source_yoffset

class TileFileSpecification:
    output = None
    width = -1
    height = -1
    tiles = []
    
    def __init__(self, output, width, height, tiles):
        self.output = output
        self.width = width
        self.height = height
        self.tiles = tiles
        
def tilenumber_to_box(image_width, image_height, tile_number, xoffset = 0, yoffset = 0):
    tile_width = image_width / 32
    #tile_height = image_height / 32
    tile_row = tile_number / tile_width
    tile_column = tile_number % tile_width
    return (tile_column * 32 + xoffset, tile_row * 32 + yoffset, tile_column * 32 + 32 + xoffset, tile_row * 32 + 32 + yoffset)

def as_transfer(entry):
    return TileTransfer(entry['filename'], source_tile = entry['source-tile'],
                        target_tile = entry['target-tile'] if 'target-tile' in entry else -1,
                        source_xoffset = entry['source-x-offset'] if 'source-x-offset' in entry else 0,
                        source_yoffset = entry['source-y-offset'] if 'source-y-offset' in entry else 0)

def as_tilefilespec(entry, verbose = False):
    return TileFileSpecification(entry['output'], entry['width'], entry['height'], [as_transfer(x) for x in entry['tiles']])

def parse_tilefilespec(tilefile, verbose = False):
      with open(tilefile) as f:
        data = json.load(f)
        return [as_tilefilespec(x) for x in data]

def process_tilespec(entry, outfile, verbose = False):
    output = Image.new('RGBA', (entry.width, entry.height), (255,0,0,255))

    last_index = -1
    for input_spec in entry.tiles:
        with Image.open(input_spec.filename) as input:
            original = tilenumber_to_box(input.width, input.height, input_spec.source_tile,
                                         xoffset=input_spec.source_xoffset,
                                         yoffset=input_spec.source_yoffset)
            region = input.crop(original)
            to_target = input_spec.target_tile
            if to_target < 0:
                to_target = last_index + 1
            target = tilenumber_to_box(output.width, output.height, tile_number = to_target)
            last_index = to_target
            output.paste(region, target)
            
    if verbose:
        print "Writing to", outfile
        
    output.save(outfile, "png")
