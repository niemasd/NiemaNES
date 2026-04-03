#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) ROM ROM Dump in iNES Format
'''

# imports
from enum import Enum
from niemanes.common import open_file
from pathlib import Path
from zipfile import ZipFile

# constants
NES_TAG = b'NES\x1A'

# screen mirroring enum
class Mirroring(Enum):
    Unknown = 0
    FourScreen = 1
    Vertical = 2
    Horizontal = 3

# class to represent complete NES ROM
class ROM:
    # initialize ROM object: https://bugzmanov.github.io/nes_ebook/chapter_5.html
    def __init__(self, data):
        # parse iNES header
        if data[0:4] != NES_TAG:
            raise ValueError('ROM is missing iNES "NES^Z" string at beginning')
        mapper = (data[7] & 0b11110000) | (data[6] >> 4)
        ines_version = (data[7] >> 2) & 0b11
        if ines_version != 0:
            raise ValueError("iNES 2.0 format is not supported")
        four_screen = (data[6] & 0b1000) != 0
        vertical_mirroring = (data[6] & 0b1) != 0
        if four_screen:
            screen_mirroring = Mirroring.FourScreen
        elif vertical_mirroring:
            screen_mirroring = Mirroring.Vertical
        else:
            screen_mirroring = Mirroring.Horizontal
        prg_rom_size = data[4] * 0x4000
        chr_rom_size = data[5] * 0x2000
        skip_trainer = (data[6] & 0b100) != 0
        prg_rom_start = 16
        if skip_trainer:
            prg_rom_start += 512
        chr_rom_start = prg_rom_start + prg_rom_size

        # set instance variables
        self.prg_rom = data[prg_rom_start : prg_rom_start + prg_rom_size]
        self.chr_rom = data[chr_rom_start : chr_rom_start + chr_rom_size]
        self.mapper = mapper
        self.screen_mirroring = screen_mirroring

    # load a game rom ROM
    def load_rom(path):
        if isinstance(path, str):
            path = Path(path)
        if path.suffix.lower().strip() == '.zip':
            with ZipFile(path, 'r') as z:
                for entry in z.infolist():
                    if entry.filename.strip().lower().endswith('.nes'):
                        return ROM(z.read(entry.filename))
            raise ValueError("No .nes files found in: %s" % path)
        else:
            with open_file(path, mode='rb') as f:
                return ROM(f.read())

# run tests
if __name__ == "__main__":
    from sys import argv
    assert len(argv) == 2, "USAGE: %s <rom.nes>" % argv[0]
    rom = ROM.load_rom(argv[1])
    print("PRG ROM Size: %s" % len(rom.prg_rom))
    print("CHR ROM Size: %s" % len(rom.chr_rom))
    print("Mapper: %s" % rom.mapper)
    print("Screen Mirroring: %s" % rom.screen_mirroring)
