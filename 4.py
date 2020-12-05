"""
--- Day 4: Passport Processing ---

You arrive at the airport only to realize that you grabbed your North Pole Credentials instead of your passport. While these documents are extremely similar, North Pole Credentials aren't issued by a country and therefore aren't actually valid documentation for travel in most of the world.
It seems like you're not the only one having problems, though; a very long line has formed for the automatic passport scanners, and the delay could upset your travel itinerary.
Due to some questionable network security, you realize you might be able to solve both of these problems at the same time.
The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.
Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).
The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.
The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.
According to the above rules, your improved system would report 2 valid passports.
Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?

--- Part Two ---

The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!
You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

[... Truncated - See example on adventofcode website ...]
Count the number of valid passports - those that have all required fields and valid values. Continue to treat cid as optional. In your batch file, how many passports are valid?

"""

import sys
import re

from collections import Counter

required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
valid_ecls = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def split_field(field):
    return field.split(':')


def parse_passport(passport_string):
    p = passport_string.split()
    return list(map(split_field, p))


def is_valid_passport_simple(passport):
    fields_present = [f[0] for f in passport]
    for required_field in required_fields:
        if required_field not in fields_present:
            return False
    return True


def is_valid_passport_complex(passport):
    fields_present = [f[0] for f in passport]
    for required_field in required_fields:
        if required_field not in fields_present:
            return False

    is_valid = True
    for (field, value) in passport:
        if field == "byr":
            is_valid = is_valid and is_year_valid(value, 1920, 2002)
        elif field == "iyr":
            is_valid = is_valid and is_year_valid(value, 2010, 2020)
        elif field == "eyr":
            is_valid = is_valid and is_year_valid(value, 2020, 2030)
        elif field == "hgt":
            is_valid = is_valid and is_hgt_valid(value)
        elif field == "hcl":
            is_valid = is_valid and is_hcl_valid(value)
        elif field == "ecl":
            is_valid = is_valid and is_ecl_valid(value)
        elif field == "pid":
            is_valid = is_valid and is_pid_valid(value)
    return is_valid

### Complex validations


def is_year_valid(year, validity_start, validity_end):
    if re.match(r'\d{4}$', year) and int(year) >= validity_start and int(year) <= validity_end:
        return True
    else:
        return False


def is_hgt_valid(hgt):
    if len(hgt) < 4:
        return False
    elif hgt[-2:] == "cm":
        height = int(hgt[:-2])
        if height >= 150 and height <= 193:
            return True
        else:
            return False
    elif hgt[-2:] == "in":
        height = int(hgt[:-2])
        if height >= 59 and height <= 76:
            return True
        else:
            return False


def is_hcl_valid(hcl):
    return bool(re.match(r'#\w{6}$', hcl))


def is_ecl_valid(ecl):
    return ecl in valid_ecls


def is_pid_valid(pid):
    return bool(re.match(r'\d{9}$', pid))

### End complex validations


def count_valid_passports(passports, validation_func):
    count = 0
    for passport in passports:
        if validation_func(passport):
            count += 1
    return count


lines = []
cache = ""
for line in sys.stdin:
    if line == '\n':
        lines.append(parse_passport(cache[:-1]))
        cache = ""
    else:
        cache += line.rstrip('\n') + " "

# add last
lines.append(parse_passport(cache[:-1]))

print("Answer 1: " + str(count_valid_passports(lines, is_valid_passport_simple)))
print("Answer 2: " + str(count_valid_passports(lines, is_valid_passport_complex)))
