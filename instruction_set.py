import loggy

class InstructionSet:

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

    def __init__(self):
            # Initialize the dictionary property
            self._instructions = {}

    def addInstruction( self, operator, description ):
        if ( operator in self._instructions ):
            loggy.log ( loggy.LOG_ERROR, operator + " already exists in instruction set" )
            return False
        else:
            json = { 
                "operator": operator, 
                "description": description, 
                "addressing_modes": {} 
            }
            
            self._instructions[operator] = json

            return True
    

    # Check if it is an instruction
    def isInstruction( self, operator ):
        if ( operator in self._instructions ):
            return True
        else:
            return False


    # Get instruction
    def getInstruction( self, operator ):
        if ( operator in self._instructions ):
            return self._instructions[operator]
        else:
            return None

    
    # Add opcode to the language
    def addOpcode( self, operator, addressing_mode, opcode ):
        
        if ( operator in self._instructions ):
            instruction = self._instructions[ operator ]
            
            if ( addressing_mode in instruction["addressing_modes"] ):
                print ( "Duplicate addressing mode " + operator )
            else:
                instruction["addressing_modes"][addressing_mode] = opcode


    def get_instruction_length(self, addressing_mode):
        instruction_length = 0
        mode = int(addressing_mode)

        if ( mode == self.addressing_mode_Implied ):
            instruction_length = 1
        elif( mode == self.addressing_mode_Accumulator):
            instruction_length = 1
        elif( mode == self.addressing_mode_Indexed_Indirect_X ):
            instruction_length = 2
        elif( mode == self.addressing_mode_Indirect_Indexed_Y ):
            instruction_length = 2
        elif( mode == self.addressing_mode_Immediate ):
            instruction_length = 2
        elif( mode == self.addressing_mode_Relative ):
            instruction_length = 2
        elif( mode == self.addressing_mode_ZeroPageX ):
            instruction_length = 2
        elif( mode == self.addressing_mode_ZeroPageY ):
            instruction_length = 2
        elif( mode == self.addressing_mode_ZeroPage ):
            instruction_length = 2
        elif( mode == self.addressing_mode_AbsoluteX ):
            instruction_length = 3
        elif( mode == self.addressing_mode_AbsoluteY ):
            instruction_length = 3
        elif( mode == self.addressing_mode_Absolute ):
            instruction_length = 3
        elif( mode == self.addressing_mode_Indirect ):
            instruction_length = 3

        return instruction_length

    def loadInstructions(self):

        self.addInstruction( "ADC","Add Memory to Accumulator with Carry")
        self.addInstruction( "AND","'AND' Memory with Accumulator")
        self.addInstruction( "ASL","Shift Left One Bit (Memory or Accumulator)")
        self.addInstruction( "BCC","Branch on Carry Clear")
        self.addInstruction( "BCS","Branch on Carry Set")
        self.addInstruction( "BEQ","Branch on Result Zero")
        self.addInstruction( "BIT","Test Bits in Memory with Accumulator")
        self.addInstruction( "BMI","Branch on Result Minus")
        self.addInstruction( "BNE","Branch on Result not Zero")
        self.addInstruction( "BPL","Branch on Result Plus")
        self.addInstruction( "BRK","Force Break")
        self.addInstruction( "BVC","Branch on Overflow Clear")
        self.addInstruction( "BVS","Branch on Overflow Set")
        self.addInstruction( "CLC","Clear Carry Flag")
        self.addInstruction( "CLD","Clear Decimal Mode")
        self.addInstruction( "CLI","Clear interrupt Disable Bit")
        self.addInstruction( "CLV","Clear Overflow Flag")
        self.addInstruction( "CMP","Compare Memory and Accumulator")
        self.addInstruction( "CPX","Compare Memory and Index X")
        self.addInstruction( "CPY","Compare Memory and Index Y")
        self.addInstruction( "DEC","Decrement Memory by One")
        self.addInstruction( "DEX","Decrement Index X by One")
        self.addInstruction( "DEY","Decrement Index Y by One")
        self.addInstruction( "EOR","'Exclusive-Or' Memory with Accumulator")
        self.addInstruction( "INC","Increment Memory by One")
        self.addInstruction( "INX","Increment Index X by One")
        self.addInstruction( "INY","Increment Index Y by One")
        self.addInstruction( "JMP","Jump to New Location")
        self.addInstruction( "JSR","Jump to New Location Saving Return Address")
        self.addInstruction( "LDA","Load Accumulator with Memory")
        self.addInstruction( "LDX","Load Index X with Memory")
        self.addInstruction( "LDY","Load Index Y with Memory") 
        self.addInstruction( "LSR","Shift Right One Bit (Memory or Accumulator) ")
        self.addInstruction( "NOP","No Operation")
        self.addInstruction( "ORA","'OR' Memory with Accumulator")
        self.addInstruction( "PHA","Push Accumulator on Stack")
        self.addInstruction( "PHP","Push Processor Status on Stack")
        self.addInstruction( "PLA","Pull Accumulator from Stack") 
        self.addInstruction( "PLP","Pull Processor Status from Stack") 
        self.addInstruction( "ROL","Rotate One Bit Left (Memory or Accumulator)") 
        self.addInstruction( "ROR","Rotate One Bit Right (Memory or Accumulator)")
        self.addInstruction( "RTI","Return from Interrupt")
        self.addInstruction( "RTS","Return from Subroutine")
        self.addInstruction( "SBC","Subtract Memory from Accumulator with Borrow")
        self.addInstruction( "SEC","Set Carry Flag")
        self.addInstruction( "SED","Set Decimal Mode") 
        self.addInstruction( "SEI","Set Interrupt Disable Status")
        self.addInstruction( "STA","Store Accumulator in Memory ")
        self.addInstruction( "STX","Store Index X in Memory")
        self.addInstruction( "STY","Store Index Y in Memory")  
        self.addInstruction( "TAX","Transfer Accumulator to Index X")
        self.addInstruction( "TAY","Transfer Accumulator to Index Y")  
        self.addInstruction( "TSX","Transfer Stack Pointer to Index X")
        self.addInstruction( "TXA","Transfer Index X to Accumulator")
        self.addInstruction( "TXS","Transfer Index X to Stack Pointer")
        self.addInstruction( "TYA","Transfer Index Y to Accumulator")

        # ADC
        self.addOpcode( "ADC", self.addressing_mode_Immediate, 0x69)
        self.addOpcode( "ADC", self.addressing_mode_ZeroPage, 0x65)
        self.addOpcode( "ADC",self.addressing_mode_ZeroPageX, 0x75)
        self.addOpcode( "ADC",self.addressing_mode_Absolute, 0x60)
        self.addOpcode( "ADC",self.addressing_mode_AbsoluteX, 0x70)
        self.addOpcode( "ADC",self.addressing_mode_AbsoluteY, 0x79)
        self.addOpcode( "ADC",self.addressing_mode_Indexed_Indirect_X, 0x61)
        self.addOpcode( "ADC",self.addressing_mode_Indirect_Indexed_Y, 0x71)

        # AND
        self.addOpcode( "AND",self.addressing_mode_Immediate, 0x29)
        self.addOpcode( "AND",self.addressing_mode_ZeroPage, 0x25)
        self.addOpcode( "AND",self.addressing_mode_ZeroPageX, 0x35)
        self.addOpcode( "AND",self.addressing_mode_Absolute, 0x2D)
        self.addOpcode( "AND",self.addressing_mode_AbsoluteX, 0x3D)
        self.addOpcode( "AND",self.addressing_mode_AbsoluteY, 0x39)
        self.addOpcode( "AND",self.addressing_mode_Indexed_Indirect_X, 0x21)
        self.addOpcode( "AND",self.addressing_mode_Indirect_Indexed_Y, 0x31)

        # ASL
        self.addOpcode( "ASL",self.addressing_mode_Accumulator, 0x0A)
        self.addOpcode( "ASL",self.addressing_mode_ZeroPage, 0x06)
        self.addOpcode( "ASL",self.addressing_mode_ZeroPageX, 0x16)
        self.addOpcode( "ASL",self.addressing_mode_Absolute, 0x0E)
        self.addOpcode( "ASL",self.addressing_mode_AbsoluteX, 0x1E)

        # Branching
        self.addOpcode( "BCC",self.addressing_mode_Relative, 0x90)
        self.addOpcode( "BCS",self.addressing_mode_Relative, 0xB0)
        self.addOpcode( "BEQ",self.addressing_mode_Relative, 0xF0)
        self.addOpcode( "BMI",self.addressing_mode_Relative, 0x30)
        self.addOpcode( "BNE",self.addressing_mode_Relative, 0xD0)
        self.addOpcode( "BPL",self.addressing_mode_Relative, 0x10)
        self.addOpcode( "BVC",self.addressing_mode_Relative, 0x50)
        self.addOpcode( "BVS",self.addressing_mode_Relative, 0x70)

        # BIT
        self.addOpcode( "BIT",self.addressing_mode_ZeroPage, 0x24)
        self.addOpcode( "BIT",self.addressing_mode_Absolute, 0x2C)

        # BRK
        self.addOpcode( "BRK",self.addressing_mode_Implied, 0x00)

        # Clear flags
        self.addOpcode( "CLC",self.addressing_mode_Implied, 0x18)
        self.addOpcode( "CLD",self.addressing_mode_Implied, 0xD8)
        self.addOpcode( "CLI",self.addressing_mode_Implied, 0x58)
        self.addOpcode( "CLV",self.addressing_mode_Implied, 0xB8)

        # CMP
        self.addOpcode( "CMP",self.addressing_mode_Immediate, 0xC9)
        self.addOpcode( "CMP",self.addressing_mode_ZeroPage, 0xC5)
        self.addOpcode( "CMP",self.addressing_mode_ZeroPageX, 0xD5)
        self.addOpcode( "CMP",self.addressing_mode_Absolute, 0xCD)
        self.addOpcode( "CMP",self.addressing_mode_AbsoluteX, 0xDD)
        self.addOpcode( "CMP",self.addressing_mode_AbsoluteY, 0xD9)
        self.addOpcode( "CMP",self.addressing_mode_Indexed_Indirect_X, 0xC1)
        self.addOpcode( "CMP",self.addressing_mode_Indirect_Indexed_Y, 0xD1)

        # CPX
        self.addOpcode( "CPX",self.addressing_mode_Immediate, 0xE0)
        self.addOpcode( "CPX",self.addressing_mode_ZeroPage, 0xE4)
        self.addOpcode( "CPX",self.addressing_mode_Absolute, 0xEC)

        # CPY
        self.addOpcode( "CPY",self.addressing_mode_Immediate, 0xC0)
        self.addOpcode( "CPY",self.addressing_mode_ZeroPage, 0xC4)
        self.addOpcode( "CPY",self.addressing_mode_Absolute, 0xCC)

        # DEC
        self.addOpcode( "DEC",self.addressing_mode_ZeroPage, 0xC6)
        self.addOpcode( "DEC",self.addressing_mode_ZeroPageX, 0xD6)
        self.addOpcode( "DEC",self.addressing_mode_Absolute, 0xCE)
        self.addOpcode( "DEC",self.addressing_mode_AbsoluteX, 0xDE)

        # DEX
        self.addOpcode( "DEX",self.addressing_mode_Implied, 0xCA)

        # DEY
        self.addOpcode( "DEY",self.addressing_mode_Implied, 0x88)

        # EOR
        self.addOpcode( "EOR",self.addressing_mode_Immediate, 0x49)
        self.addOpcode( "EOR",self.addressing_mode_ZeroPage, 0x45)
        self.addOpcode( "EOR",self.addressing_mode_ZeroPageX, 0x55)
        self.addOpcode( "EOR",self.addressing_mode_Absolute, 0x40)
        self.addOpcode( "EOR",self.addressing_mode_AbsoluteX, 0x50)
        self.addOpcode( "EOR",self.addressing_mode_AbsoluteY, 0x59)
        self.addOpcode( "EOR",self.addressing_mode_Indexed_Indirect_X, 0x41)
        self.addOpcode( "EOR",self.addressing_mode_Indirect_Indexed_Y, 0x51)

        # INC
        self.addOpcode( "INC",self.addressing_mode_ZeroPage, 0xE6)
        self.addOpcode( "INC",self.addressing_mode_ZeroPageX, 0xF6)
        self.addOpcode( "INC",self.addressing_mode_Absolute, 0xEE)
        self.addOpcode( "INC",self.addressing_mode_AbsoluteX, 0xFE)
        self.addOpcode( "INX",self.addressing_mode_Implied, 0xE8)
        self.addOpcode( "INY",self.addressing_mode_Implied, 0xC8)

        # JMP
        self.addOpcode( "JMP",self.addressing_mode_Absolute, 0x4C)
        self.addOpcode( "JMP",self.addressing_mode_Indirect, 0x6C)

        # JSR
        self.addOpcode( "JSR",self.addressing_mode_Absolute, 0x20)

        # LDA
        self.addOpcode( "LDA",self.addressing_mode_Immediate, 0xA9)
        self.addOpcode( "LDA",self.addressing_mode_ZeroPage, 0xA5)
        self.addOpcode( "LDA",self.addressing_mode_ZeroPageX, 0xB5)
        self.addOpcode( "LDA",self.addressing_mode_Absolute, 0xAD)
        self.addOpcode( "LDA",self.addressing_mode_AbsoluteX, 0xBD)
        self.addOpcode( "LDA",self.addressing_mode_AbsoluteY, 0xB9)
        self.addOpcode( "LDA",self.addressing_mode_Indexed_Indirect_X, 0xA1)
        self.addOpcode( "LDA",self.addressing_mode_Indirect_Indexed_Y, 0xB1)

        # LDX
        self.addOpcode( "LDX",self.addressing_mode_Immediate, 0xA2)
        self.addOpcode( "LDX",self.addressing_mode_ZeroPage, 0xA6)
        self.addOpcode( "LDX",self.addressing_mode_ZeroPageY, 0xB6)
        self.addOpcode( "LDX",self.addressing_mode_Absolute, 0xAE)
        self.addOpcode( "LDX",self.addressing_mode_AbsoluteY, 0xBE)

        # LDY
        self.addOpcode( "LDY",self.addressing_mode_Immediate, 0xA0)
        self.addOpcode( "LDY",self.addressing_mode_ZeroPage, 0xA4)
        self.addOpcode( "LDY",self.addressing_mode_ZeroPageX, 0xB4)
        self.addOpcode( "LDY",self.addressing_mode_Absolute, 0xAC)
        self.addOpcode( "LDY",self.addressing_mode_AbsoluteX, 0xBC)

        # LSR
        self.addOpcode( "LSR",self.addressing_mode_Accumulator, 0x4A)
        self.addOpcode( "LSR",self.addressing_mode_ZeroPage, 0x46)
        self.addOpcode( "LSR",self.addressing_mode_ZeroPageX, 0x56)
        self.addOpcode( "LSR",self.addressing_mode_Absolute, 0x4E)
        self.addOpcode( "LSR",self.addressing_mode_AbsoluteX, 0x5E)

        # NOP
        self.addOpcode( "NOP",self.addressing_mode_Implied, 0xEA)

        # ORA
        self.addOpcode( "ORA",self.addressing_mode_Immediate, 0x09)
        self.addOpcode( "ORA",self.addressing_mode_ZeroPage, 0x05)
        self.addOpcode( "ORA",self.addressing_mode_ZeroPageX, 0x15)
        self.addOpcode( "ORA",self.addressing_mode_Absolute, 0x0D)
        self.addOpcode( "ORA",self.addressing_mode_AbsoluteX, 0x10)
        self.addOpcode( "ORA",self.addressing_mode_AbsoluteY, 0x19)
        self.addOpcode( "ORA",self.addressing_mode_Indexed_Indirect_X, 0x01)
        self.addOpcode( "ORA",self.addressing_mode_Indirect_Indexed_Y, 0x11)

        # Push/Pop
        self.addOpcode( "PHA",self.addressing_mode_Implied, 0x48)
        self.addOpcode( "PHP",self.addressing_mode_Implied, 0x08)
        self.addOpcode( "PLA",self.addressing_mode_Implied, 0x68)
        self.addOpcode( "PLP",self.addressing_mode_Implied, 0x28)

        # ROL
        self.addOpcode( "ROL",self.addressing_mode_Accumulator, 0x2A)
        self.addOpcode( "ROL",self.addressing_mode_ZeroPage, 0x26)
        self.addOpcode( "ROL",self.addressing_mode_ZeroPageX, 0x36)
        self.addOpcode( "ROL",self.addressing_mode_Absolute, 0x2E)
        self.addOpcode( "ROL",self.addressing_mode_AbsoluteX, 0x3E)

        # ROR
        self.addOpcode( "ROR",self.addressing_mode_Accumulator, 0x6A)
        self.addOpcode( "ROR",self.addressing_mode_ZeroPage, 0x66)
        self.addOpcode( "ROR",self.addressing_mode_ZeroPageX, 0x76)
        self.addOpcode( "ROR",self.addressing_mode_Absolute, 0x6E)
        self.addOpcode( "ROR",self.addressing_mode_AbsoluteX, 0x7E)

        # RTI
        self.addOpcode( "RTI",self.addressing_mode_Implied, 0x4D)

        # RTS
        self.addOpcode( "RTS",self.addressing_mode_Implied, 0x60)

        # SBC
        self.addOpcode( "SBC",self.addressing_mode_Immediate, 0xE9)
        self.addOpcode( "SBC",self.addressing_mode_ZeroPage, 0xE5)
        self.addOpcode( "SBC",self.addressing_mode_ZeroPageX, 0xF5)
        self.addOpcode( "SBC",self.addressing_mode_Absolute, 0xED)
        self.addOpcode( "SBC",self.addressing_mode_AbsoluteX, 0xFD)
        self.addOpcode( "SBC",self.addressing_mode_AbsoluteY, 0xF9)
        self.addOpcode( "SBC",self.addressing_mode_Indexed_Indirect_X, 0xE1)
        self.addOpcode( "SBC",self.addressing_mode_Indirect_Indexed_Y, 0xF1)

        # SEC
        self.addOpcode( "SEC",self.addressing_mode_Implied, 0x38)

        # SED
        self.addOpcode( "SED",self.addressing_mode_Implied, 0xF8)

        # SEI
        self.addOpcode( "SEI",self.addressing_mode_Implied, 0x78)

        # STA
        self.addOpcode( "STA",self.addressing_mode_ZeroPage, 0x85)
        self.addOpcode( "STA",self.addressing_mode_ZeroPageX, 0x95)
        self.addOpcode( "STA",self.addressing_mode_Absolute, 0x8D)
        self.addOpcode( "STA",self.addressing_mode_AbsoluteX, 0x9D)
        self.addOpcode( "STA",self.addressing_mode_AbsoluteY, 0x99)
        self.addOpcode( "STA",self.addressing_mode_Indexed_Indirect_X, 0x81)
        self.addOpcode( "STA",self.addressing_mode_Indirect_Indexed_Y, 0x91)

        # STX
        self.addOpcode( "STX",self.addressing_mode_ZeroPage, 0x86)
        self.addOpcode( "STX",self.addressing_mode_ZeroPageY, 0x96)
        self.addOpcode( "STX",self.addressing_mode_Absolute, 0x8E)

        # STY
        self.addOpcode( "STY",self.addressing_mode_ZeroPage, 0x84)
        self.addOpcode( "STY",self.addressing_mode_ZeroPageX, 0x94)
        self.addOpcode( "STY",self.addressing_mode_Absolute, 0x8C)

        # Transfer
        self.addOpcode( "TAX",self.addressing_mode_Implied, 0xAA)
        self.addOpcode( "TAY",self.addressing_mode_Implied, 0xA8)
        self.addOpcode( "TSX",self.addressing_mode_Implied, 0xBA)
        self.addOpcode( "TXA",self.addressing_mode_Implied, 0x8A)
        self.addOpcode( "TXS",self.addressing_mode_Implied, 0x9A)
        self.addOpcode( "TYA",self.addressing_mode_Implied, 0x98)