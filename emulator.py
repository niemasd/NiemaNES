#! /usr/bin/env python3
'''
Run the NiemaNES emulator
'''

# imports
from niemanes import NES
from pathlib import Path
import argparse

# parse user args
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=True, type=str, help="Game ROM (.nes)")
    args = parser.parse_args()
    args.input = Path(args.input)
    if not args.input.is_file():
        raise ValueError("File not found: %s" % args.input)
    return args

# run program
if __name__ == "__main__":
    args = parse_args()
    nes = NES()
    nes.load_cartridge(args.input)
    pass # TODO
