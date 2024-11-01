#! /bin/bash

UNITPATH=./tests/*.py

grep --no-filename 'def\s.*\(.*\)\:' *.py | while read line;
do
    filter=`echo "${line}" | sed "s/def //g" | awk -F'\(' '{print $1}'`

    present=`grep -s $filter $UNITPATH`

    if [ "$present" = "" ]; then
        echo "Missing coverage for ${filter}"
    fi
done