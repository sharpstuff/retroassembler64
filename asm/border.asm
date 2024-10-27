	LDX #$00
loop:
	STX $d020
	INX
	CPX #$10
	BNE loop
	LDX #$00
	JMP loop
	RTS
