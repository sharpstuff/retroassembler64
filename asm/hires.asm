setup:
    LDA #$00
    STA $FB
    LDA #$20
    STA $FC

bitmapon:
    LDA #$08
    ORA $D018
    STA $D018
    LDA #$20
    ORA $D011
    STA $D011

    LDA #$00
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
    CPX #$3F
    BNE clrloop
    RTS