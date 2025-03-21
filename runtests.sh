#! /bin/bash

UNITPATH=./tests/*.py

echo "* Missing coverage *"

ls -1 *.py | while read file;
do
    echo "File: $file"
    grep --no-filename 'def\s.*\(.*\)\:' $file | grep -v '__init__' | while read line;
    do
        filter=`echo "${line}" | sed "s/def //g" | awk -F'\(' '{print $1}'`

        present=`grep $filter $UNITPATH`

        if [ "$present" = "" ]; then
            echo "    ${filter}"
        fi
    done
    echo ""
done

echo "Testing Instruction Set"
python3 tests/instruction_set_unit.py

echo "Testing Parser"
python3 tests/assembly_parser_unit.py

echo "Testing Assembler"
python3 tests/assembler_unit.py

