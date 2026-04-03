#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) Console
'''

# imports
from niemanes.cartridge import load_rom
from niemanes.cpu import CPU

# class to represent NES console
class NES:
    # initialize NES object
    def __init__(self):
        self.cpu = CPU(nes=self)

    # load game cartridge
    def load_cartridge(self, path):
        self.cartridge = load_rom(path)
