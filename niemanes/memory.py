#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) Memory
'''

# imports
from numpy import uint8, zeros

# class to represent complete NES memory
class Memory:
    # initialize Memory object
    def __init__(self):
        self.data = zeros(0x10000, dtype=uint8)

    # implement basic operators
    def __getitem__(self, i):
        if not isinstance(i, slice):
            i = uint16(i)
        return self.data[i]
    def __setitem__(self, i, x):
        if not isinstance(i, slice):
            i = uint16(i)
        self.data[i] = x
    def __len__(self):
        return len(self.data)
