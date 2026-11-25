#!/usr/bin/env python3
# Abhay Kumar - Roll No. 2501730185
"""
assembler.py - Hack assembler (Nand to Tetris, Capstone Part B)

Usage:  python assembler.py Prog.asm [Prog.hack]

Roll no. 2501730185  ->  K = 85  ->  K mod 3 = 1
Extra feature: a wrong line prints a clear message with its line number
(e.g. "Line 7: invalid instruction ...") instead of crashing.
"""
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- tables
PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
              "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})

# computation bits c1..c6 (the 'a' bit is added below)
_COMP_BITS = {
    "0": "101010", "1": "111111", "-1": "111010",
    "D": "001100", "A": "110000", "!D": "001101", "!A": "110001",
    "-D": "001111", "-A": "110011", "D+1": "011111", "A+1": "110111",
    "D-1": "001110", "A-1": "110010", "D+A": "000010", "D-A": "010011",
    "A-D": "000111", "D&A": "000000", "D|A": "010101",
}
COMP = {}
for _mnemonic, _bits in _COMP_BITS.items():
    COMP[_mnemonic] = "0" + _bits                       # a = 0  (uses A)
    if "A" in _mnemonic:
        COMP[_mnemonic.replace("A", "M")] = "1" + _bits  # a = 1  (uses M)

DEST = {"": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AsmError(Exception):
    """Problem with one source line (message explains what is wrong)."""


# ---------------------------------------------------------------- helpers
def clean(raw):
    """Remove comments and all whitespace from one source line."""
    return "".join(raw.split("//")[0].split())


def first_pass(lines, symbols, errors):
    """Pass 1: record the ROM address of every (LABEL)."""
    rom_address = 0
    for num, raw in enumerate(lines, start=1):
        line = clean(raw)
        if not line:
            continue
        if line.startswith("("):
            name = line[1:-1]
            if not line.endswith(")") or not SYMBOL_RE.match(name):
                errors.append(f"Line {num}: invalid label '{raw.strip()}'")
            elif name in symbols:
                errors.append(f"Line {num}: label '{name}' is already defined")
            else:
                symbols[name] = rom_address
        else:
            rom_address += 1


def translate_a(line, symbols, state):
    value = line[1:]
    if value == "":
        raise AsmError("'@' must be followed by a number or a symbol")
    if value.isascii() and value.isdigit():
        number = int(value)
        if number > 32767:
            raise AsmError(f"address {number} is too big (maximum is 32767)")
    elif SYMBOL_RE.match(value):
        if value not in symbols:                 # new variable
            symbols[value] = state["next_var"]
            state["next_var"] += 1
        number = symbols[value]
    else:
        raise AsmError(f"'{value}' is not a valid number or symbol name")
    return format(number, "016b")


def translate_c(line):
    rest, jump = (line.split(";", 1) + [""])[:2] if ";" in line else (line, "")
    dest, comp = rest.split("=", 1) if "=" in rest else ("", rest)

    if comp == "":
        raise AsmError("missing computation part")
    if comp not in COMP:
        raise AsmError(f"unknown computation '{comp}'")
    if dest not in DEST:
        raise AsmError(f"unknown destination '{dest}'")
    if jump not in JUMP:
        raise AsmError(f"unknown jump '{jump}'")
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]


def second_pass(lines, symbols, errors):
    """Pass 2: translate every instruction into 16 bits."""
    state = {"next_var": 16}
    output = []
    for num, raw in enumerate(lines, start=1):
        line = clean(raw)
        if not line or line.startswith("("):
            continue
        try:
            if line.startswith("@"):
                output.append(translate_a(line, symbols, state))
            else:
                output.append(translate_c(line))
        except AsmError as problem:
            errors.append(f"Line {num}: invalid instruction "
                          f"'{raw.strip()}' - {problem}")
    return output


def assemble(lines):
    symbols = dict(PREDEFINED)
    errors = []
    first_pass(lines, symbols, errors)
    output = second_pass(lines, symbols, errors)
    return output, errors


# ---------------------------------------------------------------- main
def main(argv):
    if len(argv) < 2:
        print("Usage: python assembler.py Prog.asm [Prog.hack]")
        return 2
    source = Path(argv[1])
    target = Path(argv[2]) if len(argv) > 2 else source.with_suffix(".hack")

    try:
        lines = source.read_text(encoding="utf-8-sig").splitlines()
    except OSError as problem:
        print(f"Cannot read '{source}': {problem}")
        return 1

    output, errors = assemble(lines)
    if errors:
        for message in errors:
            print(message)
        print(f"{len(errors)} error(s) found - {target.name} was not written.")
        return 1

    target.write_text("\n".join(output) + "\n", encoding="utf-8", newline="\n")
    print(f"OK: {source.name} -> {target.name} ({len(output)} instructions)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
