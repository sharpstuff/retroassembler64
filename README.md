# Retroassembler64

# Overview

This is a 6510 assembler that will generate binaries that will run on the Commodore 64.  As with many of these projects it starts off with a proof of concept and escalates to obsession-status and we go from there.

This is my first 6510 assembler, and indeed my first <any sort of> compiler/assembler, so the big caveat is that there may be concepts and ideas here that are generally avoided.  But, it works! 

## Usage

`python3 retroassembler.py Input assembly file [arguments]`

## Arguments
* -base 0xC000
* -output Output binary file
* -log Log Level, Diagnostic = 3, Info = 2, Warnings = 1, Errors = 0]
* -nowrite Do not write output
