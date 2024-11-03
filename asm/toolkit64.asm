; Parameters
P_CURSOR_X = $FB              ; Cursor X position
P_CURSOR_Y = $FC              ; Cursor Y position
P_STRING_L = $FB
P_STRING_H = $FC

UNUSED1 = $FD
UNUSED2 = $FE

; Memory
TEXT_MEM_START = $0400        ; Memory for text screen
TEXT_MEM_END = $07E8          ; Memory for text screen

; Characters
SPACE_CHAR = #$20
ACE_CHAR = #$41

; User

    LDA <STR
    STA P_STRING_L
    LDA >STR
    STA P_STRING_H
    JSR print_string

    RTS


STR:    .string "Hello world"

print_string:

    LDA <TEXT_MEM_START
    STA $FD
    LDA >TEXT_MEM_START
    STA $FE

    LDA #ACE_CHAR        ; What we are storing with STA
    LDY #$00             ; Needs to stay at zero
ps_clr:
    LDX $FE
    CPX >TEXT_MEM_END
    BNE ps_clr_not_finished
    LDX $FD
    CPX <TEXT_MEM_END
    BEQ ps_clr_done
ps_clr_not_finished:
    STA ($FD),Y         ;
ps_clr_wrap_check_screen:
    LDX #$FF
    CPX $FD
    BEQ ps_clr_wrap_screen
    INC $FD             ; Increment low order address
    JMP ps_clr
ps_clr_wrap_screen:
    LDX #$00            ; Wrap the low order byte
    STX $FD             ; reset the low order byte
    INC $FE             ; Increment the high order byte
    JMP ps_clr
ps_clr_done:
    LDA #$00
    STA $D3
    STA $D6
    RTS


clear_screen:
    LDA <TEXT_MEM_START
    STA $FB
    LDA >TEXT_MEM_START
    STA $FC

    LDA #SPACE_CHAR      ; What we are storing with STA
    LDY #$00             ; Needs to stay at zero
clr:
    LDX $FC
    CPX >TEXT_MEM_END
    BNE clr_not_finished
    LDX $FB
    CPX <TEXT_MEM_END
    BEQ clr_done
clr_not_finished:
    STA ($FB),Y         ; Clear the byte (accumulator)
clr_wrap_check:
    LDX #$FF
    CPX $FB
    BEQ clr_wrap
    INC $FB             ; Increment low order address
    JMP clr
clr_wrap:
    LDX #$00            ; Wrap the low order byte
    STX $FB             ; reset the low order byte
    INC $FC             ; Increment the high order byte
    JMP clr
clr_done:
    LDA #$00
    STA $D3
    STA $D6
    RTS


set_cursor:
    LDA P_CURSOR_X            ; Load the X-coordinate
    STA $D3                   ; Store it to hardware address (example address)
    LDA P_CURSOR_Y            ; Load the Y-coordinate
    STA $D6                   ; Store it to hardware address (example address)
    RTS                       ; Return from subroutine