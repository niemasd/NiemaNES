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

        # CPU instructions: https://www.nesdev.org/wiki/Instruction_reference
        self.instructions = [
            None, # 0x00 BRK 7
            None, # 0x01 ORA izx 6
            None, # 0x02 *KIL
            None, # 0x03 *SLO izx 8
            None, # 0x04 *NOP zp 3
            None, # 0x05 ORA zp 3
            None, # 0x06 ASL zp 5
            None, # 0x07 *SLO zp 5
            None, # 0x08 PHP 3
            None, # 0x09 ORA imm 2
            None, # 0x0A ASL 2
            None, # 0x0B *ANC imm 2
            None, # 0x0C *NOP abs 4
            None, # 0x0D ORA abs 4
            None, # 0x0E ASL abs 6
            None, # 0x0F *SLO abs 6
            None, # 0x10 BPL rel 2*
            None, # 0x11 ORA izy 5*
            None, # 0x12 *KIL
            None, # 0x13 *SLO izy 8
            None, # 0x14 *NOP zpx 4
            None, # 0x15 ORA zpx 4
            None, # 0x16 ASL zpx 6
            None, # 0x17 *SLO zpx 6
            None, # 0x18 CLC 2
            None, # 0x19 ORA aby 4*
            None, # 0x1A *NOP 2
            None, # 0x1B *SLO aby 7
            None, # 0x1C *NOP abx 4*
            None, # 0x1D ORA abx 4*
            None, # 0x1E ASL abx 7
            None, # 0x1F *SLO abx 7
            None, # 0x20 JSR abs 6
            None, # 0x21 AND izx 6
            None, # 0x22 *KIL
            None, # 0x23 *RLA izx 8
            None, # 0x24 BIT zp 3
            None, # 0x25 AND zp 3
            None, # 0x26 ROL zp 5
            None, # 0x27 *RLA zp 5
            None, # 0x28 PLP 4
            None, # 0x29 AND imm 2
            None, # 0x2A ROL 2
            None, # 0x2B *ANC imm 2
            None, # 0x2C BIT abs 4
            None, # 0x2D AND abs 4
            None, # 0x2E ROL abs 6
            None, # 0x2F *RLA abs 6
            None, # 0x30 BMI rel 2*
            None, # 0x31 AND izy 5*
            None, # 0x32 *KIL
            None, # 0x33 *RLA izy 8
            None, # 0x34 *NOP zpx 4
            None, # 0x35 AND zpx 4
            None, # 0x36 ROL zpx 6
            None, # 0x37 *RLA zpx 6
            None, # 0x38 SEC 2
            None, # 0x39 AND aby 4*
            None, # 0x3A *NOP 2
            None, # 0x3B *RLA aby 7
            None, # 0x3C *NOP abx 4*
            None, # 0x3D AND abx 4*
            None, # 0x3E ROL abx 7
            None, # 0x3F *RLA abx 7
            None, # 0x40 RTI 6
            None, # 0x41 EOR izx 6
            None, # 0x42 *KIL
            None, # 0x43 *SRE izx 8
            None, # 0x44 *NOP zp 3
            None, # 0x45 EOR zp 3
            None, # 0x46 LSR zp 5
            None, # 0x47 *SRE zp 5
            None, # 0x48 PHA 3
            None, # 0x49 EOR imm 2
            None, # 0x4A LSR 2
            None, # 0x4B *ALR imm 2
            None, # 0x4C JMP abs 3
            None, # 0x4D EOR abs 4
            None, # 0x4E LSR abs 6
            None, # 0x4F *SRE abs 6
            None, # 0x50 BVC rel 2*
            None, # 0x51 EOR izy 5*
            None, # 0x52 *KIL
            None, # 0x53 *SRE izy 8
            None, # 0x54 *NOP zpx 4
            None, # 0x55 EOR zpx 4
            None, # 0x56 LSR zpx 6
            None, # 0x57 *SRE zpx 6
            None, # 0x58 CLI 2
            None, # 0x59 EOR aby 4*
            None, # 0x5A *NOP 2
            None, # 0x5B *SRE aby 7
            None, # 0x5C *NOP abx 4*
            None, # 0x5D EOR abx 4*
            None, # 0x5E LSR abx 7
            None, # 0x5F *SRE abx 7
            None, # 0x60 RTS 6
            None, # 0x61 ADC izx 6
            None, # 0x62 *KIL
            None, # 0x63 *RRA izx 8
            None, # 0x64 *NOP zp 3
            None, # 0x65 ADC zp 3
            None, # 0x66 ROR zp 5
            None, # 0x67 *RRA zp 5
            None, # 0x68 PLA 4
            None, # 0x69 ADC imm 2
            None, # 0x6A ROR 2
            None, # 0x6B *ARR imm 2
            None, # 0x6C JMP ind 5
            None, # 0x6D ADC abs 4
            None, # 0x6E ROR abs 6
            None, # 0x6F *RRA abs 6
            None, # 0x70 BVS rel 2*
            None, # 0x71 ADC izy 5*
            None, # 0x72 *KIL
            None, # 0x73 *RRA izy 8
            None, # 0x74 *NOP zpx 4
            None, # 0x75 ADC zpx 4
            None, # 0x76 ROR zpx 6
            None, # 0x77 *RRA zpx 6
            None, # 0x78 SEI 2
            None, # 0x79 ADC aby 4*
            None, # 0x7A *NOP 2
            None, # 0x7B *RRA aby 7
            None, # 0x7C *NOP abx 4*
            None, # 0x7D ADC abx 4*
            None, # 0x7E ROR abx 7
            None, # 0x7F *RRA abx 7
            None, # 0x80 *NOP imm 2
            None, # 0x81 STA izx 6
            None, # 0x82 *NOP imm 2
            None, # 0x83 *SAX izx 6
            None, # 0x84 STY zp 3
            None, # 0x85 STA zp 3
            None, # 0x86 STX zp 3
            None, # 0x87 *SAX zp 3
            None, # 0x88 DEY 2
            None, # 0x89 *NOP imm 2
            None, # 0x8A TXA 2
            None, # 0x8B *XAA imm 2
            None, # 0x8C STY abs 4
            None, # 0x8D STA abs 4
            None, # 0x8E STX abs 4
            None, # 0x8F *SAX abs 4
            None, # 0x90 BCC rel 2*
            None, # 0x91 STA izy 6
            None, # 0x92 *KIL
            None, # 0x93 *AHX izy 6
            None, # 0x94 STY zpx 4
            None, # 0x95 STA zpx 4
            None, # 0x96 STX zpy 4
            None, # 0x97 *SAX zpy 4
            None, # 0x98 TYA 2
            None, # 0x99 STA aby 5
            None, # 0x9A TXS 2
            None, # 0x9B *TAS aby 5
            None, # 0x9C *SHY abx 5
            None, # 0x9D STA abx 5
            None, # 0x9E *SHX aby 5
            None, # 0x9F *AHX aby 5
            None, # 0xA0 LDY imm 2
            None, # 0xA1 LDA izx 6
            None, # 0xA2 LDX imm 2
            None, # 0xA3 *LAX izx 6
            None, # 0xA4 LDY zp 3
            None, # 0xA5 LDA zp 3
            None, # 0xA6 LDX zp 3
            None, # 0xA7 *LAX zp 3
            None, # 0xA8 TAY 2
            None, # 0xA9 LDA imm 2
            None, # 0xAA TAX 2
            None, # 0xAB *LAX imm 2
            None, # 0xAC LDY abs 4
            None, # 0xAD LDA abs 4
            None, # 0xAE LDX abs 4
            None, # 0xAF *LAX abs 4
            None, # 0xB0 BCS rel 2*
            None, # 0xB1 LDA izy 5*
            None, # 0xB2 *KIL
            None, # 0xB3 *LAX izy 5*
            None, # 0xB4 LDY zpx 4
            None, # 0xB5 LDA zpx 4
            None, # 0xB6 LDX zpy 4
            None, # 0xB7 *LAX zpy 4
            None, # 0xB8 CLV 2
            None, # 0xB9 LDA aby 4*
            None, # 0xBA TSX 2
            None, # 0xBB *LAS aby 4*
            None, # 0xBC LDY abx 4*
            None, # 0xBD LDA abx 4*
            None, # 0xBE LDX aby 4*
            None, # 0xBF *LAX aby 4*
            None, # 0xC0 CPY imm 2
            None, # 0xC1 CMP izx 6
            None, # 0xC2 *NOP imm 2
            None, # 0xC3 *DCP izx 8
            None, # 0xC4 CPY zp 3
            None, # 0xC5 CMP zp 3
            None, # 0xC6 DEC zp 5
            None, # 0xC7 *DCP zp 5
            None, # 0xC8 INY 2
            None, # 0xC9 CMP imm 2
            None, # 0xCA DEX 2
            None, # 0xCB *AXS imm 2
            None, # 0xCC CPY abs 4
            None, # 0xCD CMP abs 4
            None, # 0xCE DEC abs 6
            None, # 0xCF *DCP abs 6
            None, # 0xD0 BNE rel 2*
            None, # 0xD1 CMP izy 5*
            None, # 0xD2 *KIL
            None, # 0xD3 *DCP izy 8
            None, # 0xD4 *NOP zpx 4
            None, # 0xD5 CMP zpx 4
            None, # 0xD6 DEC zpx 6
            None, # 0xD7 *DCP zpx 6
            None, # 0xD8 CLD 2
            None, # 0xD9 CMP aby 4*
            None, # 0xDA *NOP 2
            None, # 0xDB *DCP aby 7
            None, # 0xDC *NOP abx 4*
            None, # 0xDD CMP abx 4*
            None, # 0xDE DEC abx 7
            None, # 0xDF *DCP abx 7
            None, # 0xE0 CPX imm 2
            None, # 0xE1 SBC izx 6
            None, # 0xE2 *NOP imm 2
            None, # 0xE3 *ISC izx 8
            None, # 0xE4 CPX zp 3
            None, # 0xE5 SBC zp 3
            None, # 0xE6 INC zp 5
            None, # 0xE7 *ISC zp 5
            None, # 0xE8 INX 2
            None, # 0xE9 SBC imm 2
            None, # 0xEA NOP 2
            None, # 0xEB *SBC imm 2
            None, # 0xEC CPX abs 4
            None, # 0xED SBC abs 4
            None, # 0xEE INC abs 6
            None, # 0xEF *ISC abs 6
            None, # 0xF0 BEQ rel 2*
            None, # 0xF1 SBC izy 5*
            None, # 0xF2 *KIL
            None, # 0xF3 *ISC izy 8
            None, # 0xF4 *NOP zpx 4
            None, # 0xF5 SBC zpx 4
            None, # 0xF6 INC zpx 6
            None, # 0xF7 *ISC zpx 6
            None, # 0xF8 SED 2
            None, # 0xF9 SBC aby 4*
            None, # 0xFA *NOP 2
            None, # 0xFB *ISC aby 7
            None, # 0xFC *NOP abx 4*
            None, # 0xFD SBC abx 4*
            None, # 0xFE INC abx 7
            None, # 0xFF *ISC abx            
        ]

    # interpret program
    def interpret(self):
        while True:
            orig_PC = self.PC.get()
            opcode = self.nes.memory[orig_PC]
            self.PC.set(orig_PC + 1)
            instruction = self.instructions[opcode]
            if instruction is None:
                raise NotImplementedError(f"Missing opcode: 0x{opcode:02X}")
            instruction()
            exit() # TODO DELETE

# run tests
if __name__ == "__main__":
    from niemanes.nes import NES
    cpu = CPU(nes=NES())
    pass # TODO
