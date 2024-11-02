; Parameters
PARAM_CURSOR_X = $FB          ; Cursor X position
PARAM_CURSOR_Y = $FC          ; Cursor Y position

; Memory
TEXT_MEM_START = $0400        ; Memory for text screen
TEXT_MEM_END = $07E8          ; Memory for text screen

; Characters
SPACE_CHAR = $20

    JSR clear_screen
    RTS

clear_screen:
    LDA <TEXT_MEM_START
    STA $FB
    LDA >TEXT_MEM_START
    STA $FC

    LDA SPACE_CHAR      ; What we are storing with STA
    LDY #$00            ; Needs to stay at zero
clr:
    LDX $FB
    CPX <TEXT_MEM_END
    BNE clr_not_finished
    LDX $FC
    CPX >TEXT_MEM_END
    BEQ clr_done
clr_not_finished:
    STA ($FB),Y         ; Clear the byte (accumulator)
clr_wrap_check:
    LDX #$FF
    CPX $FB
    BNE clr_no_wrap
    LDX #$00            ; Wrap the low order byte
    STA $FB
    INC $FC             ; Increment the high order byte
clr_no_wrap:
    INC $FB             ; Increment low order address
    JMP clr
clr_done:
    ;LDA #$00
    ;STA $D011
    ;STA $D012
    RTS


set_cursor:
    LDA PARAM_CURSOR_X        ; Load the X-coordinate
    STA $D011                 ; Store it to hardware address (example address)
    LDA PARAM_CURSOR_Y        ; Load the Y-coordinate
    STA $D012                 ; Store it to hardware address (example address)
    RTS                       ; Return from subroutine