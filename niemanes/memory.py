#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) Memory
'''

# imports
from numpy import uint8, uint16, zeros

# class to represent memory
class Memory:
    # initialize Memory object
    def __init__(self, size):
        self.data = zeros(size, dtype=uint8)

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

# class to represent main NES memory
class MainMemory(Memory):
    # initialize MainMemory object
    def __init__(self):
        super().__init__(size=0x10000)
    
    # fix index to handle mirroring 0x0000 - 0x2000 mirroring
    def fix_index(i):
        if not isinstance(i, slice) and i < 0x2000:
            return i & 0b11111111111
        else:
            return i
    def __getitem__(self, i):
        return super().__getitem__(MainMemory.fix_index(i))
    def __setitem__(self, i, x):
        super().__setitem__(MainMemory.fix_index(i), x)

# class to represent NES VRAM
class VRAM(Memory):
    # initialize VRAM object
    def __init__(self):
        super().__init__(size=0x800)
