.org $c000
    JMP go
    .include    "asm/included.asm"

go:
    JSR inc
    RTS