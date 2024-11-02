import re
import argparse
import loggy
import os

import instruction_set
import assembly_parser

# Notes:
# https://c64os.com/post/6502instructions

class Assembler:

    # Modes
    MODE_PRESCAN = 0
    MODE_ASSEMBLE = 1

    # Constructor (of sorts)
    def __init__(self):

        self._working_directory = os.getcwd()

        self._instruction_set = instruction_set.InstructionSet()
        self._instruction_set.loadInstructions()

        self._parser = assembly_parser.AssemblyParser()

        self.reset()


    # reset the assembler
    def reset(self):
        self._base_address = 0xC000
        self._address = 0xC000
        self._labels = {}
        self._assembly_output = bytearray()

        self._machine_code_line = ""
        self._assembly_line = ""


    # Dump assembly line
    def dump_assembly( self, address ):

        tab = max(30 - len(self._machine_code_line),0)

        str = "$" + '{:04x}'.format(address).upper() + "  "
        str = str + self._machine_code_line.upper()
        str = str + " " * tab

        str = str + self._assembly_line + " "
        loggy.log( loggy.LOG_INFO, str )

        self._assembly_line = ""
        self._machine_code_line = ""
    

    # Calculate offset for relative addressing mode
    def calculate_relative_offset(self, current_address, target_address):
        
        # Calculate the difference between the target address and the address after the branch instruction (current + 2)
        offset = target_address - current_address - 2

        # The offset must be within the range of -128 to 127 (signed 8-bit value)
        if offset < -128 or offset > 127:
            raise ValueError("Offset out of range for relative addressing (-128 to +127).")

        # Convert to an 8-bit signed value (two's complement)
        if offset < 0:
            offset = (256 + offset)  # Convert to two's complement for negative values

        return offset

    # Set the working directory of the input file
    def set_working_directory( self, directory ):
        
        self._working_directory = directory

        loggy.log( loggy.LOG_DIAGNOSTIC, "Setting working directory - " + directory )


    # Parse implied instructions with no operands, i.e. RTS, BRK, INX etc.
    def parse_implied_instruction( self, current_instruction ):
    
        # Assemble the instruction
        opcode = current_instruction["addressing_modes"][self._instruction_set.addressing_mode_Implied]
        self._assembly_output.append(opcode)
        self._assembly_line = self._assembly_line + current_instruction["operator"]
        self._machine_code_line = self._machine_code_line + '{:02x}'.format(opcode) + "       "


    # Parse label declaration, i.e. 'foo:' preceding a line with an instruction on it
    def parse_label_declaration( self, label_name ):
        if ( label_name in self._labels.keys() ):
            loggy.log( loggy.LOG_ERROR, "[!] Duplicate label " + label_name )
            exit(1)
        else:
            self._labels[label_name] = '${:04x}'.format(self._address)
            loggy.log(loggy.LOG_DIAGNOSTIC, "Stored label " + label_name + " as " + self._labels[label_name] )


    # Parse variable declaration, i.e. 'FOO = 5'
    def parse_variable_declaration( self, variable_name, token ):
        if ( variable_name in self._labels.keys() ):
            loggy.log( loggy.LOG_ERROR, "[!] Duplicate variable " + variable_name )
            exit(1)
        else:
            loggy.log(loggy.LOG_DIAGNOSTIC, "Stored variable " + variable_name + " as " + token )
            self._labels[variable_name] = token


    # Parse label references, i.e. where variables / labels are used as operands like JMP foo
    def parse_label_reference( self, match, mode ):

        loggy.log(loggy.LOG_DIAGNOSTIC, 'Label store = ' + str(self._labels))

        # Store original declaration, in the case of < and > modifiers this is useful
        orig_label = match

        # Check for high/low byte modifier
        if ( self._parser.is_high_low_byte_extract(orig_label) ):
            match = match.replace("<", "").replace(">","")
            loggy.log( loggy.LOG_DIAGNOSTIC, "Label without high/low modifier is: " + match )

        # Check whether match exists in our label store
        if ( match in self._labels.keys() ):
            
            # Resolve the label
            match = self._labels[match]
            
            # If we are modifying then use original label
            if ( self._parser.is_high_low_byte_extract(orig_label) ):
                byte = self._parser.extract_high_low_byte( orig_label, match )
                match = "#$" + '{:02x}'.format(byte)
                
            loggy.log( loggy.LOG_DIAGNOSTIC, "Resolved label/variable reference: " + match )
        else:

            if ( mode == self.MODE_PRESCAN ):
                # If we are modifying then only output will be byte literal, so assume that for now
                # so we can derive addressing mode and instruction length
                if ( self._parser.is_high_low_byte_extract(orig_label) ):
                    match = "#$00"
                else:
                    # Otherwise let's assume that if this reference is not yet defined then it isn't
                    # a variable, and so must be a label so treat as an address
                    match = "$" + '{:04x}'.format(self._address)

                loggy.log( loggy.LOG_DIAGNOSTIC, "Label not yet defined in first parse, so placeholder for now " + match )

            elif ( mode == self.MODE_ASSEMBLE ):
                loggy.log( loggy.LOG_ERROR, "Unresolved label/variable reference: " + match )
                exit(1)

        return match
            

    # Parse a relative address and turn a reference to 16 bit address to a byte  
    def parse_relative_address( self, match, current_instruction_address, mode ):

        if ( self._parser.is_word(match) ):
            relative_offset = self.calculate_relative_offset( current_instruction_address, int( "0x" + match.replace("$",""),16 ) )
            match = "$" + '{:02x}'.format(relative_offset)
            loggy.log(loggy.LOG_DIAGNOSTIC, "Resolved relative addressing: " + match )
        else:
            if ( mode == self.MODE_ASSEMBLE ):
                loggy.log( loggy.LOG_DIAGNOSTIC, "unresolved relative addressing: " + match )
                exit(1)
            elif ( mode == self.MODE_PRESCAN ):
                match = "$00"
        
        return match


    # Parse assembly directive to instruct what address assembly output should be addressed at
    def parse_org_directive( self, matches, idx ):
        # next token
        idx = idx + 1
        token = matches[idx]

        if ( self._parser.is_word( token ) ):
            self._base_address = self._parser.word_to_int(token)
            self._address = self._base_address
            loggy.log( loggy.LOG_INFO, "Setting origin to " + str(hex(self._address)) )
        else:
            loggy.log( loggy.LOG_ERROR, "Invalid origin " + token )
            exit(1)

        return idx

    
    # Parse a series of 16 bit words, used to store arbitrary strings of words in assembly output
    def parse_wordstring( self, instruction_address, matches, idx, mode ):
        
        while ( idx + 1 < len(matches) and self._parser.is_word( matches[idx+1] ) ):
            idx = idx + 1
            match = matches[idx]
            bytes = self._parser.parse_word_big_endian(match)
            
            for b in bytes:
                if ( mode == self.MODE_ASSEMBLE ):
                    self._assembly_output.append(b)
                    self._machine_code_line = self._machine_code_line + '{:02x}'.format(b) + " "
                    self._assembly_line = self._assembly_line + match + " "
                self._address = self._address + 2
        
        return idx


    # Parse a series of 8 bit bytes, used to store arbitrary strings of bytes in assembly output
    def parse_bytestring( self, instruction_address, matches, idx, mode ):
        
        while ( idx + 1 < len(matches) and self._parser.is_byte( matches[idx+1] ) ):
            idx = idx + 1
            match = matches[idx]
            bytes = self._parser.parse_byte(match)
            for b in bytes:
                if ( mode == self.MODE_ASSEMBLE ):
                    self._assembly_output.append(b)
                    self._assembly_line = self._assembly_line + match + " "
                    self._machine_code_line = self._machine_code_line + '{:02x}'.format(b) + " "
                self._address = self._address + 1

        return idx


    def parse_string(self, instruction_address, matches, idx, mode ):
        idx = idx + 1
        match = matches[idx]

        loggy.log( loggy.LOG_DIAGNOSTIC, "Parsing string " + match )
        str = match.replace("\"","")

        for char in str:
            b = ord(char)
            self._assembly_output.append(b)
            self._machine_code_line = self._machine_code_line + '{:02x}'.format(b) + " "
        
        self._machine_code_line = self._machine_code_line + '{:02x}'.format(0) + " "
        self._assembly_output.append(0)
        
        self._assembly_line = self._assembly_line + match + " "

        return idx


    def parse_include_directive(self, matches, idx ):

        include_idx = idx

        idx = idx + 1
        match = matches[idx]

        filename = match.replace("\"","")

        fullpath = os.path.join( self._working_directory, filename )

        loggy.log( loggy.LOG_DIAGNOSTIC, "Including " + fullpath + "("+filename+")" )

        if ( os.path.isfile(fullpath) ):

            with open(fullpath, "r") as source_file:
                source = source_file.read()

                # parse the file
                include_matches = self._parser.parse(source)

                # remove include directive and path
                matches.pop(include_idx)
                matches.pop(include_idx)

                elements_to_copy = len(matches) - include_idx
                included_matches_len = len(include_matches)

                # Extend matches array
                for a in range(0,included_matches_len):
                    matches.append('')
                
                copy_dest_idx = len(matches)-1
                copy_source_idx = copy_dest_idx - included_matches_len
                for b in range(0,elements_to_copy):
                    matches[copy_dest_idx] = matches[copy_source_idx]
                    
                    copy_dest_idx = copy_dest_idx - 1
                    copy_source_idx = copy_source_idx - 1
                    elements_to_copy = elements_to_copy - 1

                for match in include_matches:
                    matches[include_idx] = match
                    include_idx = include_idx + 1
        else:
            loggy.log( loggy.LOG_ERROR, "Unable to load include file: " + fullpath)
            exit()

        return idx


    # Set the base address of assembly output
    def set_base_address( self, base_address ):
        self._base_address = base_address
        self._address = base_address


    # Given instruction and addressing mode write the opcode to assembly output
    def assemble_instruction( self, current_instruction, addressing_mode, mode ):
        
        opcode = current_instruction["addressing_modes"][addressing_mode]

        loggy.log(loggy.LOG_DIAGNOSTIC, "Derived opcode " + str(opcode) )

        # Derived opcode from instruction + addressing mode, write it
        if ( mode == self.MODE_ASSEMBLE ):
            self._assembly_output.append(opcode)
            self._assembly_line = self._assembly_line + current_instruction["operator"] + " "
            self._machine_code_line = self._machine_code_line + '{:02x}'.format(opcode) + " "

        self._address = self._address + 1


    # Given operand and addressing mode write the operand to assembly output
    def assemble_operand( self, addressing_mode, match, mode ):

        # Determine instruction length based on addressing mode
        instruction_length = self._instruction_set.get_instruction_length(addressing_mode)

        if ( instruction_length == 2 ):
            loggy.log(loggy.LOG_DIAGNOSTIC, "Derived instruction length " + str(instruction_length) )

            bytes = self._parser.parse_byte(match)
            self._assembly_line = self._assembly_line + match
            for b in bytes:
                if ( mode == self.MODE_ASSEMBLE ):
                    self._assembly_output.append(b)
                    self._machine_code_line = self._machine_code_line + '{:02x}'.format(b) + "    "

            self._address = self._address + 1
        elif ( instruction_length == 3 ):  
            loggy.log(loggy.LOG_DIAGNOSTIC, "Derived instruction length " + str(instruction_length) )                          
            bytes = self._parser.parse_word_little_endian(match)
            self._assembly_line = self._assembly_line + match
            for b in bytes:
                if ( mode == self.MODE_ASSEMBLE ):
                    self._assembly_output.append(b)
                    self._machine_code_line = self._machine_code_line + '{:02x}'.format(b) + " "
                self._address = self._address + 1
        else:
            loggy.log( loggy.LOG_ERROR, "[!] Invalid instruction length " + str(instruction_length))
            exit(1)


    def preassemble( self, matches ):        

        idx = 0

        while idx < len(matches):

            match = matches[idx]

            if ( self._parser.is_org_directive( match ) ):
                
                loggy.log(loggy.LOG_DIAGNOSTIC, "Identified an .org directive on first pass" )

                # parse the address token
                idx = self.parse_org_directive( matches, idx )

            elif ( self._parser.is_include_directive( match ) ):
                
                loggy.log(loggy.LOG_DIAGNOSTIC, "Identified an .include directive on first pass" )

                # parse the address token
                idx = self.parse_include_directive( matches, idx )

                loggy.log( loggy.LOG_DIAGNOSTIC, "Post include matches - " + str(matches) )

            idx = idx + 1


    def load_source(self, filename):

        source = None

        if ( os.path.isfile(filename) ):

            with open(filename, "r") as source_file:
                self.set_working_directory(os.path.dirname(os.path.abspath(filename)))
                source = source_file.read()
        else:
            loggy.log( loggy.LOG_ERROR, "Unable to load include file: " + filename)
            exit()

        return source


    #################################################
    # Main loop for assembler!
    #################################################
    def assemble( self, matches, mode ):        

        loggy.log( loggy.LOG_DIAGNOSTIC, str(matches) )

        current_instruction = None
        idx = 0
        
        self._assembly_line = ""
        self._machine_code_line = ""

        # In run() we call set base address before the first pass, this sets address and base_address
        # We then do 1st pass assemble which updates base_address with any changes on org directive
        # So for 2nd pass assemble we do not call set_base_address so that we can ensure we don't override 
        # the above
        self._address = self._base_address

        while idx < len(matches):
            match = matches[idx]

            instruction_address = self._address

            if ( self._instruction_set.isInstruction(match) ):

                loggy.log( loggy.LOG_DIAGNOSTIC, "INSTRUCTION: " + match + " at 0x" + '{:02x}'.format(self._address) )

                # Obtain the current instruction
                current_instruction = self._instruction_set.getInstruction( match )
                current_instruction_address = self._address

                # Check for implied addressing modes that do not have an operand e.g. RTS, BRK, INC etc.
                if ( self._instruction_set.addressing_mode_Implied in current_instruction["addressing_modes"].keys() ):

                    loggy.log( loggy.LOG_DIAGNOSTIC, "Determined implied addressing: " + match )

                    if ( mode == self.MODE_ASSEMBLE ):
                        self.parse_implied_instruction( current_instruction )

                    self._address = self._address + 1

                else:
                    
                    # All other addressing modes get parsed here

                    # next token
                    idx = idx + 1
                    match = matches[idx]

                    # Resolve Labels referenced in the assembly
                    if ( self._parser.is_label_reference(match) ):

                        loggy.log( loggy.LOG_DIAGNOSTIC, "Parsed label/variable reference: " + match )

                        match = self.parse_label_reference( match, mode )
                        
                        # Check for relative addressing
                        # Note: Instructions that use relative addressing have no other addressing modes so you 
                        #       do not have to worry about any other scenarios here
                        if ( self._instruction_set.addressing_mode_Relative in current_instruction["addressing_modes"].keys() ):
        
                            loggy.log( loggy.LOG_DIAGNOSTIC, "Determined relative addressing mode, referring to : " + match )
    
                            match = self.parse_relative_address( match, current_instruction_address, mode )

                    # match addressing modes
                    for addressing_mode in current_instruction["addressing_modes"]:
                        
                        if ( self._parser.matches_addressing_mode( match, addressing_mode ) == True ):

                            loggy.log(loggy.LOG_DIAGNOSTIC, "Matched addressing mode " + str(addressing_mode) + " for " + match )

                            # Assembly step for instructions, this writes the instruction to the output!
                            self.assemble_instruction( current_instruction, addressing_mode, mode )

                            # Assembly step for operands, this writes the operand to the output!
                            self.assemble_operand( addressing_mode, match, mode )

                # If Assembling then dump output
                if ( mode == self.MODE_ASSEMBLE ):
                    self.dump_assembly( instruction_address )

            elif ( self._parser.is_bytestring_declaration(match) ):

                loggy.log(loggy.LOG_DIAGNOSTIC, "Identified a bytestring " + match )

                idx = self.parse_bytestring( instruction_address, matches, idx, mode )
                
                # If Assembling then dump output
                if ( mode == self.MODE_ASSEMBLE ):
                    self.dump_assembly( instruction_address )

            elif ( self._parser.is_wordstring_declaration(match) ):

                loggy.log(loggy.LOG_DIAGNOSTIC, "Identified a wordstring " + match )

                # Loop until we run out of words
                idx = self.parse_wordstring( instruction_address, matches, idx, mode )

                # If Assembling then dump output
                if ( mode == self.MODE_ASSEMBLE ):
                    self.dump_assembly(instruction_address )

            elif ( self._parser.is_string_declaration(match) ):

                loggy.log(loggy.LOG_DIAGNOSTIC, "Identified a string " + match )

                idx = self.parse_string( instruction_address, matches, idx, mode )
                
                # If Assembling then dump output
                if ( mode == self.MODE_ASSEMBLE ):
                    self.dump_assembly( instruction_address )

            elif ( self._parser.is_label_declaration(match) ):
                
                if ( mode == self.MODE_PRESCAN ):
                    label = match.replace(":","")

                    loggy.log(loggy.LOG_DIAGNOSTIC, "Encountered a label declaration on first pass " + label )

                    self.parse_label_declaration( label )

            elif ( self._parser.is_variable_declaration(match) ):

                if ( mode == self.MODE_PRESCAN ):
                    variable_name = self._parser.get_variable_name_from_declaration(match)
                    
                    loggy.log(loggy.LOG_DIAGNOSTIC, "Encountered a variable declaration on first pass " + variable_name )

                    # next token
                    idx = idx + 1
                    match = matches[idx]
                    
                    self.parse_variable_declaration( variable_name, match )

            else:
                loggy.log(loggy.LOG_DIAGNOSTIC, "Not processing token " + match )

            idx = idx + 1

        return self._assembly_output


    #################################################
    # Entry point for assembler!
    #################################################
    def run( self, source, base_address ):

        self.reset()

        self.set_base_address( base_address )

        # parse the file
        matches = self._parser.parse(source)

        loggy.log ( loggy.LOG_INFO, "*** Pre-process ***")
        assembly_output = self.preassemble( matches )

        loggy.log ( loggy.LOG_INFO, "*** Labels and variables ***")
        assembly_output = self.assemble( matches, self.MODE_PRESCAN )

        loggy.log ( loggy.LOG_DIAGNOSTIC, str(self._labels) )

        loggy.log ( loggy.LOG_INFO, "*** Assemble ***")
        assembly_output = self.assemble( matches, self.MODE_ASSEMBLE )

        assembly_header = bytearray( base_address.to_bytes(2, byteorder='little') )

        return assembly_header + assembly_output


