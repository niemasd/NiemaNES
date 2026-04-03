#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) Console
'''

# imports
from niemanes.cpu import CPU
from niemanes.memory import MainMemory, VRAM

# class to represent NES console
class NES:
    # initialize NES object
    def __init__(self):
        self.cpu = CPU(nes=self)
        self.memory = MainMemory()
        self.vram = VRAM()
        self.rom = None

    # load game rom
    def load_rom(self, rom):
        self.rom = rom
        if rom.mapper != 0:
            raise NotImplementedError("Games that use Mappers are not supported")
        self.memory[0x8000 : 0x10000] = memoryview(rom.prg_rom)
