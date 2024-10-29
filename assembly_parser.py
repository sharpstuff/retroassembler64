import re
import loggy

class AssemblyParser:

    ASM_REGEX_ORG_DIRECTIVE = "\.org\s?"
    ASM_REGEX_BYTESTRING_DECL = "\.byte\s?"
    ASM_REGEX_WORDSTRING_DECL = "\.word\s?"
    ASM_REGEX_VAR_DECL = "[a-zA-Z0-9]{1,20}\s*=\s*"
    ASM_REGEX_LABEL_DECL = "[a-zA-Z0-9]{1,20}:"
    ASM_REGEX_LABEL = "[<>]?[a-zA-Z0-9]{1,20}"
    ASM_REGEX_INSTRUCTION = "[a-zA-Z]{3}"
    ASM_REGEX_IMMEDIATE = "\#\$[0-9a-fA-F]{2}"
    ASM_REGEX_ABSOLUTE_X = "\$[0-9a-fA-F]{4},[X]"
    ASM_REGEX_ABSOLUTE_Y = "\$[0-9a-fA-F]{4},[Y]"
    ASM_REGEX_ABSOLUTE = "\$[0-9a-fA-F]{4}"
    ASM_REGEX_HEX8_ZEROPAGE_X = "\$[0-9a-fA-F]{2},[X]"
    ASM_REGEX_HEX8_ZEROPAGE_Y = "\$[0-9a-fA-F]{2},[Y]"
    ASM_REGEX_HEX8_ZEROPAGE = "\$[0-9a-fA-F]{2}"
    ASM_REGEX_INDIRECT_INDEXED_Y = "\(\$[0-9a-fA-F]{2}\),[Y]" # (Indirect),Y
    ASM_REGEX_INDIRECT = "\(\$[0-9a-fA-F]{4}\)"
    ASM_REGEX_INDEXED_INDIRECT_X = "\(\$[0-9a-fA-F]{2},[X]\)" # (Indirect,X)
    ASM_REGEX_RELATIVE = "\$[0-9a-fA-F]{2}"
    ASM_REGEX_ACCUMULATOR = "[A]"

    ASM_REGEX_BYTESTRING = "\$\b[0-9A-F]{2}\b(\s*,\s*\$[0-9A-F]{2})*"
    ASM_REGEX_HEX8_DIGITS = "\$[0-9a-fA-F]{2}"
    ASM_REGEX_HEX16_DIGITS = "\$[0-9a-fA-F]{4}"

    # Use these for matching tokens that are already split
    ASM_REGEX_LABEL_DECL_TOKEN = "[a-zA-Z0-9]{1,20}:$"
    ASM_REGEX_LABEL_TOKEN = "^[<>]?[a-zA-Z0-9]{1,20}$"
    ASM_REGEX_VARIABLE_DECL_TOKEN = "^[<>]?[a-zA-Z0-9]{1,20}"
    ASM_REGEX_VARIABLE_TOKEN = "^[<>]?[a-zA-Z0-9]{1,20}$"

    def __init__(self):
        # Language Patterns
        self._asm_regex_list = [
            self.ASM_REGEX_ORG_DIRECTIVE,
            self.ASM_REGEX_BYTESTRING_DECL,
            self.ASM_REGEX_WORDSTRING_DECL,
            self.ASM_REGEX_VAR_DECL,
            self.ASM_REGEX_LABEL_DECL,
            self.ASM_REGEX_LABEL,
            self.ASM_REGEX_INSTRUCTION,
            self.ASM_REGEX_IMMEDIATE,
            self.ASM_REGEX_ABSOLUTE_X,
            self.ASM_REGEX_ABSOLUTE_Y,
            self.ASM_REGEX_ABSOLUTE,
            self.ASM_REGEX_HEX8_ZEROPAGE_X,
            self.ASM_REGEX_HEX8_ZEROPAGE_Y,
            self.ASM_REGEX_HEX8_ZEROPAGE,
            self.ASM_REGEX_INDIRECT_INDEXED_Y,
            self.ASM_REGEX_INDIRECT,
            self.ASM_REGEX_INDEXED_INDIRECT_X,
            self.ASM_REGEX_RELATIVE,
            self.ASM_REGEX_ACCUMULATOR
        ]

        # Note: Order has to mirror the addressing_mode constants in mnemonics6510.py
        self._op_regex_list = [
            self.ASM_REGEX_IMMEDIATE + "$",
            self.ASM_REGEX_ABSOLUTE_X + "$",
            self.ASM_REGEX_ABSOLUTE_Y + "$",
            self.ASM_REGEX_ABSOLUTE + "$",
            self.ASM_REGEX_ACCUMULATOR + "$",
            self.ASM_REGEX_HEX8_ZEROPAGE_X + "$",
            self.ASM_REGEX_HEX8_ZEROPAGE_Y + "$",
            self.ASM_REGEX_HEX8_ZEROPAGE + "$",
            self.ASM_REGEX_INDIRECT_INDEXED_Y + "$",
            self.ASM_REGEX_INDIRECT + "$",
            self.ASM_REGEX_INDEXED_INDIRECT_X + "$",
            self.ASM_REGEX_RELATIVE + "$"
        ]

        # join to one regex
        self._asm_regex = '|'.join(self._asm_regex_list)

    # PARSING ASSEMBLY
    def parse( self, input_string ):
        matches = re.findall(self._asm_regex, input_string)
        return matches

    def matches_addressing_mode( self, token, addressing_mode ):
        match = re.match( self._op_regex_list[addressing_mode - 1], token )
        return match != None

    # PARSING OPERANDS

    def parse_byte( self, str ):
        bytes = []
        matches = re.findall( self.ASM_REGEX_HEX8_DIGITS, str )
        if ( len(matches) > 0 ):
            bytes.append( int(matches[0].replace("$", "0x"), 16) )
        return bytes

    def is_byte( self, str ):
        matches = re.findall( self.ASM_REGEX_HEX8_DIGITS, str )
        return len(matches) > 0

    def is_word( self, str ):
        matches = re.findall( self.ASM_REGEX_HEX16_DIGITS, str )
        return len(matches) > 0

    def parse_bytestring( self, str ):
        bytes = []
        matches = re.findall( self.ASM_REGEX_HEX8_DIGITS, str )
        if ( len(matches) > 0 ):
            bytes.append( int(matches[0].replace("$", "0x"), 16) )
        return bytes
    
    def parse_word_little_endian( self, str ):
        bytes = []
        matches = re.findall( self.ASM_REGEX_HEX16_DIGITS, str )
        if ( len(matches) > 0 ):
            raw_hex = matches[0].replace("$", "")
            bytes.append( int( "0x" + raw_hex[2:],16 ) )
            bytes.append( int( "0x" + raw_hex[:2],16 ) )
        return bytes
    
    def parse_word_big_endian( self, str ):
        bytes = []
        matches = re.findall( self.ASM_REGEX_HEX16_DIGITS, str )
        if ( len(matches) > 0 ):
            raw_hex = matches[0].replace("$", "")
            bytes.append( int( "0x" + raw_hex[:2],16 ) )
            bytes.append( int( "0x" + raw_hex[2:],16 ) )
        return bytes

    def word_to_int( self, word ):
        raw_hex = word.replace("$","")
        hex = "0x" + raw_hex
        return int(hex,16)

    def is_high_low_byte_extract( self, str ):
        return ( str[:1] == "<" or str[:1] == ">" )

    def extract_high_low_byte( self, label, str ):
        bytes = self.parse_word_little_endian(str)
        if ( label[:1] == "<" ):
            return bytes[0]
        elif ( label[:1] == ">" ):
            return bytes[1]
        else:
            return None
    
    # BYTESTRINGS

    def is_bytestring_declaration( self, str ):
        matches = re.findall( self.ASM_REGEX_BYTESTRING_DECL, str )
        return len(matches) > 0

    def is_wordstring_declaration( self, str ):
        matches = re.findall( self.ASM_REGEX_WORDSTRING_DECL, str )
        return len(matches) > 0

    def is_org_directive( self, str ):
        matches = re.findall( self.ASM_REGEX_ORG_DIRECTIVE, str )
        return len(matches) > 0

    # LABELS

    def is_label_declaration( self, str ):
        matches = re.findall( self.ASM_REGEX_LABEL_DECL_TOKEN, str )
        return len(matches) > 0

    def is_label_reference( self, str ):
        matches = re.findall( self.ASM_REGEX_LABEL_TOKEN, str )
        # TODO would prefer to make this cleanly identify the label with REGEX
        return len(matches) > 0 and str[:1] != "#" and str[:1] != "$"


    # VARIABLES

    def is_variable_declaration( self, str ):
        matches = re.findall( self.ASM_REGEX_VAR_DECL, str )
        return len(matches) > 0

    def is_variable_reference( self, str ):
        matches = re.findall( self.ASM_REGEX_VARIABLE_TOKEN, str )
        return len(matches) > 0

    def get_variable_name_from_declaration( self, str ):
        matches = re.findall( self.ASM_REGEX_VARIABLE_DECL_TOKEN, str )
        if ( len(matches) > 0 ):
            return matches[0]
        else:
            return None
