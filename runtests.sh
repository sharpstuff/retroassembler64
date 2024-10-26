#! /bin/bash

if [ "$(ls -A test/output/)" ]; then
	rm test/output/*
fi

./retro -o test/output/test.prg test/test.asm
./retro -t64 -o test/output/test.t64 test/test.asm
./retro -t64 -o test/output/hires.t64 test/hires.asm
./retro -t64 -o test/output/border.t64 test/border.asm
./retro -o test/output/labels.prg test/labels.asm
./retro -o test/output/text.prg test/text.asm

for f in test/output/*
do
	FILEMD5=`md5sum ${f}`
	BENCHMARK=`cat test/benchmarks | grep ${f}`

	if [ "${FILEMD5}" == "${BENCHMARK}" ]
	then
		echo "${f} PASS"
	else
		echo "${f} does not match benchmark"
		echo "Actual    - ${FILEMD5}"
		echo "Benchmark - ${BENCHMARK}" 
	fi
done
