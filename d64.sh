#! /bin/bash

../Vice/tools/c1541 \
	-format diskname,id d64 dev.d64 \
	-attach dev.d64 \
	-write test/border.prg border
