SCNKEY = $FF9F

setup:
LDA #$00
STA $FB
LDA #$04
STA $FC

LDA #$41
LDY #$00

clrloop:
STA ($FB),Y

INC $FB
LDX $FB
CPX #$FF
BNE clrloop
STA ($FB),Y
STA $FB
INC $FC
LDX $FC
CPX #$08
BNE clrloop

JSR SCNKEY

RTS
