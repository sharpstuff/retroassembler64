#! /bin/bash

FILE=$1 
OUTPUT=images/dev.d64
NAME=`echo $FILE | sed -e 's/.*\///g'`

echo "Writing $FILE name ($NAME)"


if [ ! -f $OUTPUT ]; then
	echo "No disk file, formatting $OUTPUT"
	../Vice/tools/c1541 \
		-format diskname,id d64 $OUTPUT
fi

if [ -f $FILE ]; then
	../Vice/tools/c1541 \
		-attach $OUTPUT \
		-delete $NAME

	../Vice/tools/c1541 \
		-attach $OUTPUT \
		-write $FILE
else
	echo "$FILE does not exist"
fi
