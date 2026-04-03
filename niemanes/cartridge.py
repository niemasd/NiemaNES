#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) Cartridge
'''

# imports
from niemanes.common import open_file
from pathlib import Path
from zipfile import ZipFile

# load a game cartridge ROM
def load_rom(path):
    if isinstance(path, str):
        path = Path(path)
    if path.suffix.lower().strip() == '.zip':
        with ZipFile(path, 'r') as z:
            for entry in z.infolist():
                if entry.filename.strip().lower().endswith('.nes'):
                    return Cartridge(z.read(entry.filename))
        raise ValueError("No .nes files found in: %s" % path)
    else:
        with open_file(path, mode='rb') as f:
            return Cartridge(f.read())

# class to represent complete NES cartridge
class Cartridge:
    # initialize Cartridge object
    def __init__(self, data):
        self.data = data # raw data

    # get length of cartridge (in bytes)
    def __len__(self):
        return len(self.data)

# run tests
if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 2, "USAGE: %s <rom.nes>" % argv[0]
    cartridge = load_rom(argv[1])
    print("Size: %s" % len(cartridge))
