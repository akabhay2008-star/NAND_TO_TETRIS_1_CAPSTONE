// Abhay Kumar - Roll No. 2501730185
// Box.asm  -  Roll no. 2501730185, K = 85
// While any key is pressed, draw a black box; when released, erase it.
//
// Box: starts at row 85, 20 rows tall,
//      width = 16 * ((85 mod 4) + 1) = 32 pixels = 2 words, from the left edge.
// Top-left word address = SCREEN + 32*85 = 16384 + 2720 = 19104

(MAIN)
    @KBD
    D=M
    @BLACK
    D;JNE          // key pressed -> black
    @color
    M=0            // no key -> white
    @DRAW
    0;JMP
(BLACK)
    @color
    M=-1           // -1 = 1111111111111111 = 16 black pixels

(DRAW)
    @SCREEN
    D=A
    @2720          // 32 * 85  (START ROW 85)
    D=D+A
    @addr
    M=D            // addr = first word of the top row of the box
    @20            // BOX HEIGHT = 20 rows
    D=A
    @rows
    M=D            // rows = rows left to draw

(ROWLOOP)
    @color
    D=M
    @addr
    A=M
    M=D            // word 0 of this row (pixels 0-15)
    A=A+1
    M=D            // word 1 of this row (pixels 16-31)  -> WIDTH = 2 words
    @addr
    D=M
    @32
    D=D+A          // move down one screen row (32 words)
    @addr
    M=D
    @rows
    MD=M-1
    @ROWLOOP
    D;JGT          // more rows left? repeat
    @MAIN
    0;JMP          // check the keyboard again, forever
