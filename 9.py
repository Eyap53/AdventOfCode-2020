"""
--- Day 9: Encoding Error ---

[...]

The first step of attacking the weakness in the XMAS data is to find the first number in the list (after the preamble) which is not the sum of two of the 25 numbers before it. What is the first number that does not have this property?

--- Part Two ---

[...]

What is the encryption weakness in your XMAS-encrypted list of numbers?
"""

import sys

from collections import Counter


def ParseLine(input):
    return int(input.rstrip('\n'))


def is_valid_entry(entry, previous_entries):
    """
    Check if given entry is valid.
    """
    for i in range(len(previous_entries)):
        for line2 in previous_entries[(i+1):]:
            if previous_entries[i] + line2 == entry:
                return True
        i += 1
    return False


def find_weakness(xmas_data, preamble_length):
    """
    """
    for i in range(preamble_length, len(xmas_data)):
        if not is_valid_entry(xmas_data[i], xmas_data[i-preamble_length:i]):
            return [i, xmas_data[i]]
    print("ERROR: Weakness not found")
    return [0, 0]


def add_min_max(list_values):
    """
    Add the min and max of the given list_values
    """
    return min(list_values) + max(list_values)


def exploit_weakness(invalid_entry, previous_entries):
    for i in range(len(previous_entries)):
        if previous_entries[i] == invalid_entry:
            print("Error, not supposed to happen")
        elif previous_entries[i] > invalid_entry:
            pass
        current_sum = previous_entries[i]
        j = 0
        while current_sum < invalid_entry:
            j += 1
            current_sum += previous_entries[i+j]
        if current_sum == invalid_entry:
            print("Root found : " + str(i) + " to " + str(i+j))
            return add_min_max(previous_entries[i:i+j+1])
    print("ERROR: Couldn't find exploit")
    return None


lines = []
for line in sys.stdin:
    lines.append(ParseLine(line))

weakness = find_weakness(lines, 25)
print("Weakness (index, value) : " + str(weakness))

print("Exploit : " + str(exploit_weakness(weakness[1], lines[:weakness[0]])))
