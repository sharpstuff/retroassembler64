#! /bin/bash

echo "Testing Instruction Set"
python3 tests/instruction_set_unit.py

echo "Testing Parser"
python3 tests/assembly_parser_unit.py

echo "Testing Assembler"
python3 tests/assembler_unit.py