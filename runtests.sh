#! /bin/bash

echo "Testing Instruction Set"
python3 tests/instructions_unit.py

echo "Testing Parser"
python3 tests/parse6510_unit.py

echo "Testing Assembler"
python3 tests/assembler_unit.py