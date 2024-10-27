	.org $C000

	FOO = $C000
	BAR = #$F8

	LDA FOO
	LDX BAR
loop:
	LDA <isr
	LDA >isr
	STX FOO
	INX
	CPX #$10
	BNE looper
	RTS

looper:
	JMP loop

isr:
	LDA #$65
	STA $D020
	RTS


	.byte $AA
	.word $DEAD $BEEF
	.byte $AA, $55, $AA, $55

	JMP loop