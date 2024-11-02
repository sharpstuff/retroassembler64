    .org $c000
    JMP go
    .include    "included.asm"

go:
    JSR inc
    RTS