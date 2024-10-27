import re
import loggy
import mnemonics6510

# Assembly Language Regexes
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
ASM_REGEX_INDIRECT_INDEXED_X = "\(\$[0-9a-fA-F]{2}\),[X]"
ASM_REGEX_INDIRECT_INDEXED_Y = "\(\$[0-9a-fA-F]{2}\),[Y]"
ASM_REGEX_INDIRECT = "\(\$[0-9a-fA-F]{4}\)"
ASM_REGEX_INDEXED_INDIRECT_X = "\(\$[0-9a-fA-F]{2},[X]\)"
ASM_REGEX_INDEXED_INDIRECT_Y = "\(\$[0-9a-fA-F]{2},[Y]\)"
ASM_REGEX_RELATIVE = "\$[0-9a-fA-F]{2}"
ASM_REGEX_ACCUMULATOR = "[A]"
ASM_REGEX_CRLF = "\r\n"

ASM_REGEX_BYTESTRING = "\$\b[0-9A-F]{2}\b(\s*,\s*\$[0-9A-F]{2})*"
ASM_REGEX_HEX8_DIGITS = "\$[0-9a-fA-F]{2}"
ASM_REGEX_HEX16_DIGITS = "\$[0-9a-fA-F]{4}"

# Use these for matching tokens that are already split
ASM_REGEX_LABEL_DECL_TOKEN = "[a-zA-Z0-9]{1,20}:$"
ASM_REGEX_LABEL_TOKEN = "^[<>]?[a-zA-Z0-9]{1,20}$"
ASM_REGEX_VARIABLE_DECL_TOKEN = "^[<>]?[a-zA-Z0-9]{1,20}"
ASM_REGEX_VARIABLE_TOKEN = "^[<>]?[a-zA-Z0-9]{1,20}$"


# Patterns
asm_regex_list = [
    ASM_REGEX_ORG_DIRECTIVE,
    ASM_REGEX_BYTESTRING_DECL,
    ASM_REGEX_WORDSTRING_DECL,
    ASM_REGEX_VAR_DECL,
    ASM_REGEX_LABEL_DECL,
    ASM_REGEX_LABEL,
    ASM_REGEX_INSTRUCTION,
    ASM_REGEX_IMMEDIATE,
    ASM_REGEX_ABSOLUTE_X,
    ASM_REGEX_ABSOLUTE_Y,
    ASM_REGEX_ABSOLUTE,
    ASM_REGEX_HEX8_ZEROPAGE_X,
    ASM_REGEX_HEX8_ZEROPAGE_Y,
    ASM_REGEX_HEX8_ZEROPAGE,
    ASM_REGEX_INDIRECT_INDEXED_X,
    ASM_REGEX_INDIRECT_INDEXED_Y,
    ASM_REGEX_INDIRECT,
    ASM_REGEX_INDEXED_INDIRECT_X,
    ASM_REGEX_INDEXED_INDIRECT_Y,
    ASM_REGEX_RELATIVE,
    ASM_REGEX_ACCUMULATOR,
    ASM_REGEX_CRLF
]

op_regex_list = [
    ASM_REGEX_IMMEDIATE + "$",
    ASM_REGEX_ABSOLUTE_X + "$",
    ASM_REGEX_ABSOLUTE_Y + "$",
    ASM_REGEX_ABSOLUTE + "$",
    ASM_REGEX_ACCUMULATOR + "$",
    ASM_REGEX_HEX8_ZEROPAGE_X + "$",
    ASM_REGEX_HEX8_ZEROPAGE_Y + "$",
    ASM_REGEX_HEX8_ZEROPAGE + "$",
    ASM_REGEX_INDIRECT_INDEXED_X + "$",
    ASM_REGEX_INDIRECT_INDEXED_Y + "$",
    ASM_REGEX_INDIRECT + "$",
    ASM_REGEX_INDEXED_INDIRECT_X + "$",
    ASM_REGEX_INDEXED_INDIRECT_Y + "$",
    ASM_REGEX_RELATIVE + "$"
]

# join to one regex
asm_regex = '|'.join(asm_regex_list)

# PARSING ASSEMBLY
def parse( input_string ):
    matches = re.findall(asm_regex, input_string)
    return matches

def matches_addressing_mode( token, addressing_mode ):
    match = re.match( op_regex_list[addressing_mode - 1], token )
    return match != None

# PARSING OPERANDS

def parse_byte( str ):
    bytes = []
    matches = re.findall( ASM_REGEX_HEX8_DIGITS, str )
    if ( len(matches) > 0 ):
        bytes.append( int(matches[0].replace("$", "0x"), 16) )
    return bytes

def is_byte( str ):
    matches = re.findall( ASM_REGEX_HEX8_DIGITS, str )
    return len(matches) > 0

def is_word( str ):
    matches = re.findall( ASM_REGEX_HEX16_DIGITS, str )
    return len(matches) > 0

def parse_bytestring( str ):
    bytes = []
    matches = re.findall( ASM_REGEX_HEX8_DIGITS, str )
    if ( len(matches) > 0 ):
        bytes.append( int(matches[0].replace("$", "0x"), 16) )
    return bytes
    
def parse_word_little_endian( str ):
    bytes = []
    matches = re.findall( ASM_REGEX_HEX16_DIGITS, str )
    if ( len(matches) > 0 ):
        raw_hex = matches[0].replace("$", "")
        bytes.append( int( "0x" + raw_hex[2:],16 ) )
        bytes.append( int( "0x" + raw_hex[:2],16 ) )
    return bytes
    
def parse_word_big_endian( str ):
    bytes = []
    matches = re.findall( ASM_REGEX_HEX16_DIGITS, str )
    if ( len(matches) > 0 ):
        raw_hex = matches[0].replace("$", "")
        bytes.append( int( "0x" + raw_hex[:2],16 ) )
        bytes.append( int( "0x" + raw_hex[2:],16 ) )
    return bytes

def word_to_int( word ):
    raw_hex = word.replace("$","")
    hex = "0x" + raw_hex
    return int(hex,16)

def is_high_low_byte_extract( str ):
    return ( str[:1] == "<" or str[:1] == ">" )

def extract_high_low_byte( label, str ):
    bytes = parse_word_little_endian(str)
    if ( label[:1] == "<" ):
        return bytes[0]
    elif ( label[:1] == ">" ):
        return bytes[1]
    else:
        return None
    
# BYTESTRINGS

def is_bytestring_declaration( str ):
    matches = re.findall( ASM_REGEX_BYTESTRING_DECL, str )
    return len(matches) > 0

def is_wordstring_declaration( str ):
    matches = re.findall( ASM_REGEX_WORDSTRING_DECL, str )
    return len(matches) > 0

def is_org_directive( str ):
    matches = re.findall( ASM_REGEX_ORG_DIRECTIVE, str )
    return len(matches) > 0

# LABELS

def is_label_declaration( str ):
    matches = re.findall( ASM_REGEX_LABEL_DECL_TOKEN, str )
    return len(matches) > 0

def is_label_reference( str ):
    matches = re.findall( ASM_REGEX_LABEL_TOKEN, str )
    # TODO would prefer to make this cleanly identify the label with REGEX
    return len(matches) > 0 and str[:1] != "#" and str[:1] != "$"


# VARIABLES

def is_variable_declaration( str ):
    matches = re.findall( ASM_REGEX_VAR_DECL, str )
    return len(matches) > 0

def is_variable_reference( str ):
    matches = re.findall( ASM_REGEX_VARIABLE_TOKEN, str )
    return len(matches) > 0

def get_variable_name_from_declaration( str ):
    matches = re.findall( ASM_REGEX_VARIABLE_DECL_TOKEN, str )
    if ( len(matches) > 0 ):
        return matches[0]
    else:
        return None
