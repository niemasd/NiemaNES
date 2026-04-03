#! /usr/bin/env python3
'''
Nintendo Entertainment System (NES) CPU
'''

# imports
from niemanes.common import get_bit, reset_bit, set_bit
from numpy import uint8, uint16

# constants
FLAG_C = 0 # Carry (C) flag
FLAG_Z = 1 # Zero (Z) flag
FLAG_I = 2 # Interrupt Disable (I) flag
FLAG_D = 3 # Decimal (D) flag
FLAG_B = 4 # B flag
FLAG_V = 6 # Overflow (V) flag
FLAG_N = 7 # Negative (N) flag

# class to represent a CPU register
class Register:
    # initialize Register object
    def __init__(self, value=0):
        self.set(value)

    # set value
    def set(self, value):
        self.data = value

    # get value
    def get(self):
        return self.data

# class to represent an 8-bit CPU register
class Register8(Register):
    # set value
    def set(self, value):
        self.data = uint8(value)

# class to represent Stack Pointer (SP) register
class RegisterSP(Register8):
    pass # TODO

# class to represent Processor Status (P) register
class RegisterP(Register8):
    # initialize RegisterP object
    def __init__(self, value=0b00100000):
        super().__init__(value=value)

    # get, set, and reset flags
    def get_flag(self, flag_pos):
        return get_bit(flag_pos, self.get())
    def set_flag(self, flag_pos):
        self.set(set_bit(flag_pos, self.get()))
    def reset_flag(self, flag_pos):
        self.set(reset_bit(flag_pos, self.get()))

# class to represent 16-bit CPU register
class Register16(Register):
    # set value
    def set(self, value):
        self.data = uint16(value)

# class to represent Program Counter (PC) register
class RegisterPC(Register16):
    pass # TODO

# class to represent NES CPU
class CPU:
    # initialize CPU object
    def __init__(self, nes):
        # NES console this CPU belongs to
        self.nes = nes

        # registers
        self.PC = RegisterPC() # Program Counter (PC)
        self.SP = RegisterSP() # Stack Pointer (SP)
        self.A  = Register8()  # Accumulator (A)
        self.X  = Register8()  # Index Register X (X)
        self.Y  = Register8()  # Index Register Y (Y)
        self.P  = RegisterP()  # Processor Status (P)

# run tests
if __name__ == "__main__":
    from niemanes.nes import NES
    cpu = CPU(nes=NES())
    pass # TODO
