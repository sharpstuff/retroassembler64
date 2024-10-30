import assembler
import re
import os
import argparse
import loggy

asm64 = assembler.Assembler()

# Parse the command line
def parse_command_line():
    # Create the parser
    parser = argparse.ArgumentParser(description="Assembler")
    
    # Add a filename argument
    parser.add_argument('filename', help='Input assembly file')
    parser.add_argument('-base',    help='Base address e.g. 0xC000')
    parser.add_argument('-output',  help='Filename of assembled output')
    parser.add_argument('-log',     help='Log Level, Diagnostic = 3, Info = 2, Warnings = 1, Errors = 0')
    parser.add_argument('-nowrite', help='Do not write output')

    # Parse the arguments
    args = parser.parse_args()

    # Return the filename
    return args


# generate an output filename
def generate_output_filename( filename ):
    matches = re.findall("\..*$", filename)
    if ( len(matches)>0 ):
        return filename.replace(matches[0], "" )
    else:
        return filename


# Write output to file
def write_binary_output( bytes, filename ):
    
    with open(filename, "wb") as binary_file:
        binary_file.write( bytes )
        

def start( ):

    base_address = 0xC000
    write_enabled = True

    args = parse_command_line()

    if ( "log" in args and args.log != None ):
        loggy.LOG_LEVEL = int( args.log )
        loggy.log ( loggy.LOG_DIAGNOSTIC, "Setting log level to " + str(args.log) )
    if ( "base" in args and args.base != None ):
        base_address = int(args.base, 16)
        loggy.log ( loggy.LOG_DIAGNOSTIC, "Setting base address to " + str(args.base) )
    if ( "output" in args and args.output != None ):
        output_filename = str(args.output)
        loggy.log ( loggy.LOG_DIAGNOSTIC, "Setting output filename to " + str(args.output) )
    else:
        output_filename = generate_output_filename(args.filename)
    if ( "nowrite" in args ):
        write_enabled = False

    # input file
    if ( os.path.isfile(args.filename) ):
        f = open(args.filename, "r")
        source = f.read()

        assembly_output = asm64.run(source, base_address)

        loggy.log ( loggy.LOG_INFO, "Writing to " + output_filename )
        write_binary_output( assembly_output, output_filename )

start()