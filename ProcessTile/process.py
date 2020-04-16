#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import pprint
from PIL import Image, ImageColor

class TileTransfer:
    filename = None
    source_tile = 0
    target_tile = -1
    source_xoffset = 0
    source_yoffset = 0
    transparent = None # 3 tuple rgb
    
    def __init__(self, filename, source_tile, target_tile = -1, source_xoffset = 0, source_yoffset = 0, transparent = None):
        self.filename = filename
        self.source_tile = source_tile
        self.target_tile = target_tile
        self.source_xoffset = source_xoffset
        self.source_yoffset = source_yoffset
        self.transparent = transparent

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
    tile_width = int(image_width) // 32
    #tile_height = image_height / 32
    tile_row = int(tile_number) // int(tile_width)
    tile_column = int(tile_number) % int(tile_width)
    return (int(tile_column * 32 + xoffset), int(tile_row * 32 + yoffset),
            int(tile_column * 32 + 32 + xoffset), int(tile_row * 32 + 32 + yoffset))

def possibly_make_transparent(image, box, transparent_colour):
    make_transparent(image.crop(box), transparent_colour)

def make_transparent(image, transparent_colour):
    for x in range(image.width):
        for y in range(image.height):
            pixel = image.getpixel((x,y))
            if pixel[0] == transparent_colour[0] and pixel[1] == transparent_colour[1] and pixel[2] == transparent_colour[2]:
                image.putpixel((x,y), (pixel[0],pixel[1],pixel[2],0))  

def as_colour(input):
    return ImageColor.getrgb(input)

def as_transfer(entry):
    return TileTransfer(entry['filename'], source_tile = entry['source-tile'],
                        target_tile = entry['target-tile'] if 'target-tile' in entry else -1,
                        source_xoffset = entry['source-x-offset'] if 'source-x-offset' in entry else 0,
                        source_yoffset = entry['source-y-offset'] if 'source-y-offset' in entry else 0,
                        transparent = as_colour(entry['transparent']) if 'transparent' in entry else None)
                        

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
            region = input.crop(original).convert('RGBA')
            to_target = input_spec.target_tile
            if to_target < 0:
                to_target = last_index + 1
            target = tilenumber_to_box(output.width, output.height, tile_number = to_target)
            last_index = to_target
            if input_spec.transparent:
                make_transparent(region, transparent_colour = input_spec.transparent)
            output.paste(region, target)
            
    if verbose:
        print("Writing to ", outfile)
        
    output.save(outfile, "png")
