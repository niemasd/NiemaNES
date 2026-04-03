#! /usr/bin/env python3
'''
Common variables, classes, functions, etc.
'''

# imports
from pathlib import Path

# dummy function that doesn't do anything
def dummy():
    pass

# open a file for reading/writing
def open_file(path, mode='rb'):
    if isinstance(path, str):
        path = Path(path)
    if path.suffix.strip().lower() == '.gz':
        return gopen(path, mode=mode)
    else:
        return open(path, mode=mode)

# return the n-th bit of a bool (0 = False, 1 = True)
def get_bit(bit_num, value):
    return bool((value >> bit_num) & 0x01)

# return the result of resetting the n-th bit of an integer to 0
def reset_bit(bit_num, value):
    return uint8(value & ~(0x01 << bit_num))

# return the result of setting the n-th bit of an integer to 1
def set_bit(bit_num, value):
    return uint8(value | (0x01 << bit_num))
