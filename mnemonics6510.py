instructionSet = {}

# Addressing modes
addressing_mode_Implied = 0
addressing_mode_Immediate = 1
addressing_mode_AbsoluteX = 2
addressing_mode_AbsoluteY = 3
addressing_mode_Absolute = 4
addressing_mode_Accumulator = 5
addressing_mode_ZeroPageX = 6
addressing_mode_ZeroPageY = 7
addressing_mode_ZeroPage = 8
addressing_mode_Indirect_Indexed_Y = 9
addressing_mode_Indirect = 10
addressing_mode_Indexed_Indirect_X = 11
addressing_mode_Relative = 12

# Add instruction to the language
def addInstruction( operator, description ):
    if ( operator in instructionSet ):
        print ( operator + " already exists in instruction set" )
    else:
        json = { 
            "operator": operator, 
            "description": description, 
            "addressing_modes": {} 
        }
        
        instructionSet[operator] = json

# Check if it is an instruction
def isInstruction( operator ):
    if ( operator in instructionSet ):
        return True
    else:
        return False

# Get instruction
def getInstruction( operator ):
    if ( operator in instructionSet ):
        return instructionSet[operator]
    else:
        return None
    
# Add opcode to the language
def addOpcode( operator, addressing_mode, opcode ):
    
    if ( operator in instructionSet ):
        instruction = instructionSet[ operator ]
        
        if ( addressing_mode in instruction["addressing_modes"] ):
            print ( "Duplicate addressing mode " + operator )
        else:
            instruction["addressing_modes"][addressing_mode] = opcode


def get_instruction_length(addressing_mode):
    instruction_length = 0
    mode = int(addressing_mode)

    if ( mode == addressing_mode_Implied ):
        instruction_length = 1
    elif( mode == addressing_mode_Accumulator):
        instruction_length = 1
    elif( mode == addressing_mode_Indexed_Indirect_X ):
        instruction_length = 2
    elif( mode == addressing_mode_Indirect_Indexed_Y ):
        instruction_length = 2
    elif( mode == addressing_mode_Immediate ):
        instruction_length = 2
    elif( mode == addressing_mode_Relative ):
        instruction_length = 2
    elif( mode == addressing_mode_ZeroPageX ):
        instruction_length = 2
    elif( mode == addressing_mode_ZeroPageY ):
        instruction_length = 2
    elif( mode == addressing_mode_ZeroPage ):
        instruction_length = 2
    elif( mode == addressing_mode_AbsoluteX ):
        instruction_length = 3
    elif( mode == addressing_mode_AbsoluteY ):
        instruction_length = 3
    elif( mode == addressing_mode_Absolute ):
        instruction_length = 3
    elif( mode == addressing_mode_Indirect ):
        instruction_length = 3

    return instruction_length


# add instructions
addInstruction( "ADC","Add Memory to Accumulator with Carry")
addInstruction( "AND","'AND' Memory with Accumulator")
addInstruction( "ASL","Shift Left One Bit (Memory or Accumulator)")
addInstruction( "BCC","Branch on Carry Clear")
addInstruction( "BCS","Branch on Carry Set")
addInstruction( "BEQ","Branch on Result Zero")
addInstruction( "BIT","Test Bits in Memory with Accumulator")
addInstruction( "BMI","Branch on Result Minus")
addInstruction( "BNE","Branch on Result not Zero")
addInstruction( "BPL","Branch on Result Plus")
addInstruction( "BRK","Force Break")
addInstruction( "BVC","Branch on Overflow Clear")
addInstruction( "BVS","Branch on Overflow Set")
addInstruction( "CLC","Clear Carry Flag")
addInstruction( "CLD","Clear Decimal Mode")
addInstruction( "CLI","Clear interrupt Disable Bit")
addInstruction( "CLV","Clear Overflow Flag")
addInstruction( "CMP","Compare Memory and Accumulator")
addInstruction( "CPX","Compare Memory and Index X")
addInstruction( "CPY","Compare Memory and Index Y")
addInstruction( "DEC","Decrement Memory by One")
addInstruction( "DEX","Decrement Index X by One")
addInstruction( "DEY","Decrement Index Y by One")
addInstruction( "EOR","'Exclusive-Or' Memory with Accumulator")
addInstruction( "INC","Increment Memory by One")
addInstruction( "INX","Increment Index X by One")
addInstruction( "INY","Increment Index Y by One")
addInstruction( "JMP","Jump to New Location")
addInstruction( "JSR","Jump to New Location Saving Return Address")
addInstruction( "LDA","Load Accumulator with Memory")
addInstruction( "LDX","Load Index X with Memory")
addInstruction( "LDY","Load Index Y with Memory") 
addInstruction( "LSR","Shift Right One Bit (Memory or Accumulator) ")
addInstruction( "NOP","No Operation")
addInstruction( "ORA","'OR' Memory with Accumulator")
addInstruction( "PHA","Push Accumulator on Stack")
addInstruction( "PHP","Push Processor Status on Stack")
addInstruction( "PLA","Pull Accumulator from Stack") 
addInstruction( "PLP","Pull Processor Status from Stack") 
addInstruction( "ROL","Rotate One Bit Left (Memory or Accumulator)") 
addInstruction( "ROR","Rotate One Bit Right (Memory or Accumulator)")
addInstruction( "RTI","Return from Interrupt")
addInstruction( "RTS","Return from Subroutine")
addInstruction( "SBC","Subtract Memory from Accumulator with Borrow")
addInstruction( "SEC","Set Carry Flag")
addInstruction( "SED","Set Decimal Mode") 
addInstruction( "SEI","Set Interrupt Disable Status")
addInstruction( "STA","Store Accumulator in Memory ")
addInstruction( "STX","Store Index X in Memory")
addInstruction( "STY","Store Index Y in Memory")  
addInstruction( "TAX","Transfer Accumulator to Index X")
addInstruction( "TAY","Transfer Accumulator to Index Y")  
addInstruction( "TSX","Transfer Stack Pointer to Index X")
addInstruction( "TXA","Transfer Index X to Accumulator")
addInstruction( "TXS","Transfer Index X to Stack Pointer")
addInstruction( "TYA","Transfer Index Y to Accumulator")

# ADC
addOpcode("ADC",addressing_mode_Immediate, 0x69)
addOpcode("ADC",addressing_mode_ZeroPage, 0x65)
addOpcode("ADC",addressing_mode_ZeroPageX, 0x75)
addOpcode("ADC",addressing_mode_Absolute, 0x60)
addOpcode("ADC",addressing_mode_AbsoluteX, 0x70)
addOpcode("ADC",addressing_mode_AbsoluteY, 0x79)
addOpcode("ADC",addressing_mode_Indexed_Indirect_X, 0x61)
addOpcode("ADC",addressing_mode_Indirect_Indexed_Y, 0x71)

# AND
addOpcode("AND",addressing_mode_Immediate, 0x29)
addOpcode("AND",addressing_mode_ZeroPage, 0x25)
addOpcode("AND",addressing_mode_ZeroPageX, 0x35)
addOpcode("AND",addressing_mode_Absolute, 0x2D)
addOpcode("AND",addressing_mode_AbsoluteX, 0x3D)
addOpcode("AND",addressing_mode_AbsoluteY, 0x39)
addOpcode("AND",addressing_mode_Indexed_Indirect_X, 0x21)
addOpcode("AND",addressing_mode_Indirect_Indexed_Y, 0x31)

# ASL
addOpcode("ASL",addressing_mode_Accumulator, 0x0A)
addOpcode("ASL",addressing_mode_ZeroPage, 0x06)
addOpcode("ASL",addressing_mode_ZeroPageX, 0x16)
addOpcode("ASL",addressing_mode_Absolute, 0x0E)
addOpcode("ASL",addressing_mode_AbsoluteX, 0x1E)

# Branching
addOpcode("BCC",addressing_mode_Relative, 0x90)
addOpcode("BCS",addressing_mode_Relative, 0xB0)
addOpcode("BEQ",addressing_mode_Relative, 0xF0)
addOpcode("BMI",addressing_mode_Relative, 0x30)
addOpcode("BNE",addressing_mode_Relative, 0xD0)
addOpcode("BPL",addressing_mode_Relative, 0x10)
addOpcode("BVC",addressing_mode_Relative, 0x50)
addOpcode("BVS",addressing_mode_Relative, 0x70)

# BIT
addOpcode("BIT",addressing_mode_ZeroPage, 0x24)
addOpcode("BIT",addressing_mode_Absolute, 0x2C)

# BRK
addOpcode("BRK",addressing_mode_Implied, 0x00)

# Clear flags
addOpcode("CLC",addressing_mode_Implied, 0x18)
addOpcode("CLD",addressing_mode_Implied, 0xD8)
addOpcode("CLI",addressing_mode_Implied, 0x58)
addOpcode("CLV",addressing_mode_Implied, 0xB8)

# CMP
addOpcode("CMP",addressing_mode_Immediate, 0xC9)
addOpcode("CMP",addressing_mode_ZeroPage, 0xC5)
addOpcode("CMP",addressing_mode_ZeroPageX, 0xD5)
addOpcode("CMP",addressing_mode_Absolute, 0xCD)
addOpcode("CMP",addressing_mode_AbsoluteX, 0xDD)
addOpcode("CMP",addressing_mode_AbsoluteY, 0xD9)
addOpcode("CMP",addressing_mode_Indexed_Indirect_X, 0xC1)
addOpcode("CMP",addressing_mode_Indirect_Indexed_Y, 0xD1)

# CPX
addOpcode("CPX",addressing_mode_Immediate, 0xE0)
addOpcode("CPX",addressing_mode_ZeroPage, 0xE4)
addOpcode("CPX",addressing_mode_Absolute, 0xEC)

# CPY
addOpcode("CPY",addressing_mode_Immediate, 0xC0)
addOpcode("CPY",addressing_mode_ZeroPage, 0xC4)
addOpcode("CPY",addressing_mode_Absolute, 0xCC)

# DEC
addOpcode("DEC",addressing_mode_ZeroPage, 0xC6)
addOpcode("DEC",addressing_mode_ZeroPageX, 0xD6)
addOpcode("DEC",addressing_mode_Absolute, 0xCE)
addOpcode("DEC",addressing_mode_AbsoluteX, 0xDE)

# DEX
addOpcode("DEX",addressing_mode_Implied, 0xCA)

# DEY
addOpcode("DEY",addressing_mode_Implied, 0x88)

# EOR
addOpcode("EOR",addressing_mode_Immediate, 0x49)
addOpcode("EOR",addressing_mode_ZeroPage, 0x45)
addOpcode("EOR",addressing_mode_ZeroPageX, 0x55)
addOpcode("EOR",addressing_mode_Absolute, 0x40)
addOpcode("EOR",addressing_mode_AbsoluteX, 0x50)
addOpcode("EOR",addressing_mode_AbsoluteY, 0x59)
addOpcode("EOR",addressing_mode_Indexed_Indirect_X, 0x41)
addOpcode("EOR",addressing_mode_Indirect_Indexed_Y, 0x51)

# INC
addOpcode("INC",addressing_mode_ZeroPage, 0xE6)
addOpcode("INC",addressing_mode_ZeroPageX, 0xF6)
addOpcode("INC",addressing_mode_Absolute, 0xEE)
addOpcode("INC",addressing_mode_AbsoluteX, 0xFE)
addOpcode("INX",addressing_mode_Implied, 0xE8)
addOpcode("INY",addressing_mode_Implied, 0xC8)

# JMP
addOpcode("JMP",addressing_mode_Absolute, 0x4C)
addOpcode("JMP",addressing_mode_Indirect, 0x6C)

# JSR
addOpcode("JSR",addressing_mode_Absolute, 0x20)

# LDA
addOpcode("LDA",addressing_mode_Immediate, 0xA9)
addOpcode("LDA",addressing_mode_ZeroPage, 0xA5)
addOpcode("LDA",addressing_mode_ZeroPageX, 0xB5)
addOpcode("LDA",addressing_mode_Absolute, 0xAD)
addOpcode("LDA",addressing_mode_AbsoluteX, 0xBD)
addOpcode("LDA",addressing_mode_AbsoluteY, 0xB9)
addOpcode("LDA",addressing_mode_Indexed_Indirect_X, 0xA1)
addOpcode("LDA",addressing_mode_Indirect_Indexed_Y, 0xB1)

# LDX
addOpcode("LDX",addressing_mode_Immediate, 0xA2)
addOpcode("LDX",addressing_mode_ZeroPage, 0xA6)
addOpcode("LDX",addressing_mode_ZeroPageY, 0xB6)
addOpcode("LDX",addressing_mode_Absolute, 0xAE)
addOpcode("LDX",addressing_mode_AbsoluteY, 0xBE)

# LDY
addOpcode("LDY",addressing_mode_Immediate, 0xA0)
addOpcode("LDY",addressing_mode_ZeroPage, 0xA4)
addOpcode("LDY",addressing_mode_ZeroPageX, 0xB4)
addOpcode("LDY",addressing_mode_Absolute, 0xAC)
addOpcode("LDY",addressing_mode_AbsoluteX, 0xBC)

# LSR
addOpcode("LSR",addressing_mode_Accumulator, 0x4A)
addOpcode("LSR",addressing_mode_ZeroPage, 0x46)
addOpcode("LSR",addressing_mode_ZeroPageX, 0x56)
addOpcode("LSR",addressing_mode_Absolute, 0x4E)
addOpcode("LSR",addressing_mode_AbsoluteX, 0x5E)

# NOP
addOpcode("NOP",addressing_mode_Implied, 0xEA)

# ORA
addOpcode("ORA",addressing_mode_Immediate, 0x09)
addOpcode("ORA",addressing_mode_ZeroPage, 0x05)
addOpcode("ORA",addressing_mode_ZeroPageX, 0x15)
addOpcode("ORA",addressing_mode_Absolute, 0x0D)
addOpcode("ORA",addressing_mode_AbsoluteX, 0x10)
addOpcode("ORA",addressing_mode_AbsoluteY, 0x19)
addOpcode("ORA",addressing_mode_Indexed_Indirect_X, 0x01)
addOpcode("ORA",addressing_mode_Indirect_Indexed_Y, 0x11)

# Push/Pop
addOpcode("PHA",addressing_mode_Implied, 0x48)
addOpcode("PHP",addressing_mode_Implied, 0x08)
addOpcode("PLA",addressing_mode_Implied, 0x68)
addOpcode("PLP",addressing_mode_Implied, 0x28)

# ROL
addOpcode("ROL",addressing_mode_Accumulator, 0x2A)
addOpcode("ROL",addressing_mode_ZeroPage, 0x26)
addOpcode("ROL",addressing_mode_ZeroPageX, 0x36)
addOpcode("ROL",addressing_mode_Absolute, 0x2E)
addOpcode("ROL",addressing_mode_AbsoluteX, 0x3E)

# ROR
addOpcode("ROR",addressing_mode_Accumulator, 0x6A)
addOpcode("ROR",addressing_mode_ZeroPage, 0x66)
addOpcode("ROR",addressing_mode_ZeroPageX, 0x76)
addOpcode("ROR",addressing_mode_Absolute, 0x6E)
addOpcode("ROR",addressing_mode_AbsoluteX, 0x7E)

# RTI
addOpcode("RTI",addressing_mode_Implied, 0x4D)

# RTS
addOpcode("RTS",addressing_mode_Implied, 0x60)

# SBC
addOpcode("SBC",addressing_mode_Immediate, 0xE9)
addOpcode("SBC",addressing_mode_ZeroPage, 0xE5)
addOpcode("SBC",addressing_mode_ZeroPageX, 0xF5)
addOpcode("SBC",addressing_mode_Absolute, 0xED)
addOpcode("SBC",addressing_mode_AbsoluteX, 0xFD)
addOpcode("SBC",addressing_mode_AbsoluteY, 0xF9)
addOpcode("SBC",addressing_mode_Indexed_Indirect_X, 0xE1)
addOpcode("SBC",addressing_mode_Indirect_Indexed_Y, 0xF1)

# SEC
addOpcode("SEC",addressing_mode_Implied, 0x38)

# SED
addOpcode("SED",addressing_mode_Implied, 0xF8)

# SEI
addOpcode("SEI",addressing_mode_Implied, 0x78)

# STA
addOpcode("STA",addressing_mode_ZeroPage, 0x85)
addOpcode("STA",addressing_mode_ZeroPageX, 0x95)
addOpcode("STA",addressing_mode_Absolute, 0x8D)
addOpcode("STA",addressing_mode_AbsoluteX, 0x9D)
addOpcode("STA",addressing_mode_AbsoluteY, 0x99)
addOpcode("STA",addressing_mode_Indexed_Indirect_X, 0x81)
addOpcode("STA",addressing_mode_Indirect_Indexed_Y, 0x91)

# STX
addOpcode("STX",addressing_mode_ZeroPage, 0x86)
addOpcode("STX",addressing_mode_ZeroPageY, 0x96)
addOpcode("STX",addressing_mode_Absolute, 0x8E)

# STY
addOpcode("STY",addressing_mode_ZeroPage, 0x84)
addOpcode("STY",addressing_mode_ZeroPageX, 0x94)
addOpcode("STY",addressing_mode_Absolute, 0x8C)

# Transfer
addOpcode("TAX",addressing_mode_Implied, 0xAA)
addOpcode("TAY",addressing_mode_Implied, 0xA8)
addOpcode("TSX",addressing_mode_Implied, 0xBA)
addOpcode("TXA",addressing_mode_Implied, 0x8A)
addOpcode("TXS",addressing_mode_Implied, 0x9A)
addOpcode("TYA",addressing_mode_Implied, 0x98)