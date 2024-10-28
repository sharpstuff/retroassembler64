import parse6510
import mnemonics6510
import re
import argparse
import loggy

# Notes:
# https://c64os.com/post/6502instructions

# Modes
MODE_PRESCAN = 0
MODE_ASSEMBLE = 1

def dump_assembly( address, machine_code, assembly ):

    tab = max(30 - len(machine_code),0)

    str = "$" + '{:04x}'.format(address).upper() + "  "
    str = str + machine_code.upper()
    str = str + " " * tab

    str = str + assembly + " "
    loggy.log( loggy.LOG_INFO, str )
    

# Calculate offset for relative addressing mode
def calculate_relative_offset(current_address, target_address):
    
    # Calculate the difference between the target address and the address after the branch instruction (current + 2)
    offset = target_address - current_address - 2

    # The offset must be within the range of -128 to 127 (signed 8-bit value)
    if offset < -128 or offset > 127:
        raise ValueError("Offset out of range for relative addressing (-128 to +127).")

    # Convert to an 8-bit signed value (two's complement)
    if offset < 0:
        offset = (256 + offset)  # Convert to two's complement for negative values

    return offset


def assemble( source, labels, base_address, mode ):        
    
    assembly_output = bytearray()
    
    # parse the file
    matches = parse6510.parse(source)

    loggy.log( loggy.LOG_DIAGNOSTIC, str(matches) )

    current_instruction = None
    idx = 0
    address = base_address

    while idx < len(matches):
        match = matches[idx]
        s_assembly = ""
        s_machinecode = ""

        instruction_address = address

        if ( mnemonics6510.isInstruction(match) ):

            loggy.log( loggy.LOG_DIAGNOSTIC, "INSTRUCTION: " + match )

            # Obtain the current instruction
            current_instruction = mnemonics6510.getInstruction( match )
            current_instruction_address = address

            # Check for implied addressing modes that do not have an operand e.g. RTS, BRK, INC etc.
            if ( mnemonics6510.addressing_mode_Implied in current_instruction["addressing_modes"].keys() ):

                loggy.log( loggy.LOG_DIAGNOSTIC, "Determined implied addressing: " + match )

                opcode = current_instruction["addressing_modes"][mnemonics6510.addressing_mode_Implied]
                
                # Assemble the instruction
                if ( mode == MODE_ASSEMBLE ):
                    assembly_output.append(opcode)
                    s_assembly = s_assembly + current_instruction["operator"]
                    s_machinecode = s_machinecode + '{:02x}'.format(opcode) + "       "
                address = address + 1
            else:
                
                # All other addressing modes get parsed here

                # next token
                idx = idx + 1
                match = matches[idx]

                # Resolve Labels
                if ( parse6510.is_label_reference(match) ):

                    loggy.log( loggy.LOG_DIAGNOSTIC, "Parsed label/variable reference: " + match )

                    # Store original declaration, in the case of < and > modifiers this is useful
                    orig_label = match

                    # Check for high/low byte modifier
                    if ( parse6510.is_high_low_byte_extract(orig_label) ):
                        match = match.replace("<", "").replace(">","")
                        loggy.log( loggy.LOG_DIAGNOSTIC, "Label without high/low modifier is: " + match )

                    # Check whether match exists in our label store
                    if ( match in labels.keys() ):
                        
                        # Resolve the label
                        match = labels[match]
                        
                        # If we are modifying then use original label
                        if ( parse6510.is_high_low_byte_extract(orig_label) ):
                            byte = parse6510.extract_high_low_byte( orig_label, match )
                            match = "#$" + '{:02x}'.format(byte)
                            
                        loggy.log( loggy.LOG_DIAGNOSTIC, "Resolved label/variable reference: " + match )
                    else:

                        if ( mode == MODE_PRESCAN ):
                            # If we are modifying then only output will be byte literal, so assume that for now
                            # so we can derive addressing mode and instruction length
                            if ( parse6510.is_high_low_byte_extract(orig_label) ):
                                match = "#$00"
                        elif ( mode == MODE_ASSEMBLE ):
                            loggy.log( loggy.LOG_ERROR, "Unresolved label/variable reference: " + match )
                            exit(1)
                    
                    # Check for relative addressing
                    # Note: Instructions that use relative addressing have no other addressing modes so you 
                    #       do not have to worry about any other scenarios here
                    if ( mnemonics6510.addressing_mode_Relative in current_instruction["addressing_modes"].keys() ):
    
                        loggy.log( loggy.LOG_DIAGNOSTIC, "Determined relative addressing mode, referring to : " + match )
 
                        if ( parse6510.is_word(match) ):
                            relative_offset = calculate_relative_offset( current_instruction_address, int( "0x" + match.replace("$",""),16 ) )
                            match = "$" + '{:02x}'.format(relative_offset)
                            loggy.log(loggy.LOG_DIAGNOSTIC, "Resolved relative addressing: " + match )
                        else:
                            if ( mode == MODE_ASSEMBLE ):
                                loggy.log( loggy.LOG_DIAGNOSTIC, "unresolved relative addressing: " + match )
                                exit(1)
                            elif ( mode == MODE_PRESCAN ):
                                match = "$00"

                # match addressing modes
                for addressing_mode in current_instruction["addressing_modes"]:
                    
                    if ( parse6510.matches_addressing_mode( match, addressing_mode ) == True ):

                        loggy.log(loggy.LOG_DIAGNOSTIC, "Matched addressing mode " + str(addressing_mode) + " for " + match )

                        opcode = current_instruction["addressing_modes"][addressing_mode]

                        loggy.log(loggy.LOG_DIAGNOSTIC, "Derived opcode " + str(opcode) )

                        # Derived opcode from instruction + addressing mode, write it
                        if ( mode == MODE_ASSEMBLE ):
                            assembly_output.append(opcode)
                            s_assembly = s_assembly + current_instruction["operator"] + " "
                            s_machinecode = s_machinecode + '{:02x}'.format(opcode) + " "

                        address = address + 1

                        # Determine instruction length based on addressing mode
                        ilen = mnemonics6510.get_instruction_length(addressing_mode)
                        
                        if ( ilen == 2 ):
                            loggy.log(loggy.LOG_DIAGNOSTIC, "Derived instruction length " + str(ilen) )

                            bytes = parse6510.parse_byte(match)
                            s_assembly = s_assembly + match
                            for b in bytes:
                                if ( mode == MODE_ASSEMBLE ):
                                    assembly_output.append(b)
                                    s_machinecode = s_machinecode + '{:02x}'.format(b) + "    "

                                address = address + 1
                        elif ( ilen == 3 ):  
                            loggy.log(loggy.LOG_DIAGNOSTIC, "Derived instruction length " + str(ilen) )                          
                            bytes = parse6510.parse_word_little_endian(match)
                            s_assembly = s_assembly + match
                            for b in bytes:
                                if ( mode == MODE_ASSEMBLE ):
                                    assembly_output.append(b)
                                    s_machinecode = s_machinecode + '{:02x}'.format(b) + " "
                                address = address + 1
                        else:
                            loggy.log( loggy.LOG_ERROR, "[!] Invalid instruction length " + str(ilen))
                            exit(1)

            # If Assembling then dump output
            if ( mode == MODE_ASSEMBLE ):
                dump_assembly(instruction_address, s_machinecode, s_assembly )
        elif ( parse6510.is_bytestring_declaration(match) ):

            loggy.log(loggy.LOG_DIAGNOSTIC, "Identified a bytestring " + match )

            while ( idx + 1 < len(matches) and parse6510.is_byte( matches[idx+1] ) ):
                idx = idx + 1
                match = matches[idx]
                bytes = parse6510.parse_byte(match)
                for b in bytes:
                    if ( mode == MODE_ASSEMBLE ):
                        assembly_output.append(b)
                        s_assembly = s_assembly + match + " "
                        s_machinecode = s_machinecode + '{:02x}'.format(b) + " "
                    address = address + 1
            # If Assembling then dump output
            if ( mode == MODE_ASSEMBLE ):
                dump_assembly(instruction_address, s_machinecode, s_assembly )    
        elif ( parse6510.is_wordstring_declaration(match) ):

            loggy.log(loggy.LOG_DIAGNOSTIC, "Identified a wordstring " + match )

            while ( idx + 1 < len(matches) and parse6510.is_word( matches[idx+1] ) ):
                idx = idx + 1
                match = matches[idx]
                bytes = parse6510.parse_word_big_endian(match)
                
                for b in bytes:
                    if ( mode == MODE_ASSEMBLE ):
                        assembly_output.append(b)
                        s_machinecode = s_machinecode + '{:02x}'.format(b) + " "
                    address = address + 2
                s_assembly = s_assembly + match + " "
            # If Assembling then dump output
            if ( mode == MODE_ASSEMBLE ):
                dump_assembly(instruction_address, s_machinecode, s_assembly )    
        elif ( parse6510.is_label_declaration(match) ):
            
            if ( mode == MODE_PRESCAN ):
                label = match.replace(":","")

                loggy.log(loggy.LOG_DIAGNOSTIC, "Encountered a label declaration on first pass " + label )

                if ( label in labels.keys() ):
                    loggy.log( loggy.LOG_ERROR, "[!] Duplicate label " + label )
                    exit(1)
                else:
                    labels[label] = '${:04x}'.format(address)
                    loggy.log(loggy.LOG_DIAGNOSTIC, "Stored label " + label + " as " + labels[label] )
        elif ( parse6510.is_variable_declaration(match) ):

            if ( mode == MODE_PRESCAN ):
                variable_name = parse6510.get_variable_name_from_declaration(match)
                
                loggy.log(loggy.LOG_DIAGNOSTIC, "Encountered a variable declaration on first pass " + variable_name )

                # next token
                idx = idx + 1
                match = matches[idx]
                
                if ( variable_name in labels.keys() ):
                    loggy.log( loggy.LOG_ERROR, "[!] Duplicate variable " + label )
                    exit(1)
                else:
                    loggy.log(loggy.LOG_DIAGNOSTIC, "Stored variable " + variable_name + " as " + match )
                    labels[variable_name] = match

        elif ( parse6510.is_org_directive( match ) ):
            
            if ( mode == MODE_PRESCAN ):
                
                loggy.log(loggy.LOG_DIAGNOSTIC, "Identified an .org directive on first pass" )

                # next token
                idx = idx + 1
                match = matches[idx]

                if ( parse6510.is_word( match ) ):
                    address = parse6510.word_to_int(match)
                    loggy.log( loggy.LOG_INFO, "Setting origin to " + str(hex(address)) )
                else:
                    loggy.log( loggy.LOG_ERROR, "Invalid origin " + match )
                    exit(1)

        else:
            loggy.log(loggy.LOG_DIAGNOSTIC, "Unhandled token " + match )

        idx = idx + 1

    return assembly_output


def run(source, base_address):

    labels = {}
    loggy.log ( loggy.LOG_INFO, "*** PASS 1 ***")
    binary_output = assemble( source, labels, base_address, MODE_PRESCAN )
    loggy.log ( loggy.LOG_DIAGNOSTIC, str(labels) )
    loggy.log ( loggy.LOG_INFO, "*** PASS 2 ***")
    binary_output = assemble( source, labels, base_address, MODE_ASSEMBLE )

    return binary_output


