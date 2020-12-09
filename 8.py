"""
--- Day 8: Handheld Halting ---

[...]

Run your copy of the boot code. Immediately before any instruction is executed a second time, what value is in the accumulator?

--- Part Two ---

[...]

Fix the program so that it terminates normally by changing exactly one jmp (to nop) or nop (to jmp). What is the value of the accumulator after the program terminates?
"""

import sys

from collections import Counter


def ParseLine(input):
    line = input.rstrip('\n').split()
    line[1] = int(line[1])
    return line


def check_accumulator(program_lines):
    nextLineIndex = 0
    accumulator = 0
    first_execution = [True for i in range(len(program_lines))]
    while first_execution[nextLineIndex]:
        first_execution[nextLineIndex] = False
        if program_lines[nextLineIndex][0] == "acc":
            accumulator += program_lines[nextLineIndex][1]
            nextLineIndex += 1
        elif program_lines[nextLineIndex][0] == "nop":
            nextLineIndex += 1
        elif program_lines[nextLineIndex][0] == "jmp":
            nextLineIndex += program_lines[nextLineIndex][1]
        else:
            print("ERROR: Not Recognized")
        if nextLineIndex == len(program_lines):
            return [True, accumulator]

    return [False, accumulator]


def repairProgram(program_lines):
    """
    Brute force search of solution.
    return: array of length 2:
        - First element is bool: True if solution found, false otherwise
        - Second element is int: The accumulator value (before the loop if infinite)
    """
    for i in range(len(program_lines)):
        if program_lines[i][0] == "jmp":
            program_lines[i][0] = "nop"
            result = check_accumulator(program_lines)
            if result[0]:
                return result
            else:
                program_lines[i][0] = "jmp"
        elif program_lines[i][0] == "nop":
            program_lines[i][0] = "jmp"
            result = check_accumulator(program_lines)
            if result[0]:
                return result
            else:
                program_lines[i][0] = "nop"
    return [False, 0]


lines = []
for line in sys.stdin:
    lines.append(ParseLine(line))

print(repairProgram(lines))
