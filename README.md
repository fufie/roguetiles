# RogueTiles

A small python library meant for command-line work on tiles for games in general and roguelikes in particular.

## Use Cases

## First use-case
The first use-case is to retrieve one or more tiles from one or more files and place into a new tile file.  This is meant to be scriptable so the target tile file can be re-generated at any point. 

### Example of tilesheet where we want the trees
![Original Tilesheet](examples/terrain.png)

### Sample conversion order
![Sample json-file with instructions](examples/sample-json.png)
(The image above may not be 100% up-to-date, please check json-file in `examples` for up-to-date syntax and features)

### Resulting tilesheet with just trees and shrubbery
![Resulting tilesheet](examples/trees.png)

## Second use-case
The second use-case is to extract single tiles into a single file, for later use/version control/etc.
```bash
extract-tile.py -t 498 -y 16 -i examples/terrain.png -o foo.png
```

# Installation

The code depends on Pillow (formerly PIL) so making a simple 'virtualenv' and doing 'pip install pillow' should be sufficient.

