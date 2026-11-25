# Nand to Tetris I - Capstone: Make the Computer Draw a Box

- Name: Abhay Kumar
- Roll No.: 2501730185
- Personal number: K = 85

## Personal values
- Box: starts at row 85, 20 rows tall, 32 pixels (2 words) wide from the left edge
- Top-left word address: SCREEN + 32 x 85 = 16384 + 2720 = 19104
- Assembler extra feature (K mod 3 = 1): clear error messages with line numbers

## Structure
- `Part_A_Computer/` - `CPU.hdl`, `Memory.hdl`, `Computer.hdl`
- `Part_B_Assembler/` - `assembler.py`, test programs and their `.hack` output, `Invalid.asm` (error demo)
- `Part_C_Box/` - `Box.asm`, `Box.hack` (assembled with my own assembler)
- `Screenshots/` - test and result screenshots

## Run the assembler
```
python Part_B_Assembler/assembler.py Part_C_Box/Box.asm
```
