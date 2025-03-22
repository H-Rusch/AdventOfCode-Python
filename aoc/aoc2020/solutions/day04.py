import re


# create regular expressions which search a passport for the required information
byr_regex = re.compile("byr:(\d{4})")
iyr_regex = re.compile("iyr:(\d{4})")
eyr_regex = re.compile("eyr:(\d{4})")
hgt_regex = re.compile("hgt:(\d*)(cm|in)")
hcl_regex = re.compile("hcl:#(([0-9]|[a-f]){6})")
ecl_regex = re.compile("ecl:((amb)|(blu)|(brn)|(gry)|(grn)|(hzl)|(oth))")
pid_regex = re.compile("pid:(\d*)")


def part1(input):
    passports = parse(input)

    return sum(map(check_valid, passports))


def part2(input):
    passports = parse(input)

    count = 0
    for passport in passports:
        if check_valid2(passport):
            count += 1

    return count


# passport is valid if all fields are present apart from cid
def check_valid(string):
    passport = string.replace("\n", " ")
    return all(
        info in passport for info in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    )


# passport is valid for the 2nd part if all fields are present apart from cid and the values are correct
def check_valid2(string):
    passport = string.replace("\n", " ")
    if not all(
        info in passport for info in ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    ):
        return False

    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    byr = int(byr_regex.search(passport).group(1)) in range(1920, 2003)
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    iyr = int(iyr_regex.search(passport).group(1)) in range(2010, 2021)
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    eyr = int(eyr_regex.search(passport).group(1)) in range(2020, 2031)
    # hgt (Height) - a number followed by either cm or in:
    #   If cm, the number must be at least 150 and at most 193.
    #   If in, the number must be at least 59 and at most 76.
    hgt = hgt_regex.search(passport)
    if hgt:
        if hgt.group(2) == "cm":
            hgt = int(hgt.group(1)) in range(150, 194)
        else:
            hgt = int(hgt.group(1)) in range(59, 79)

    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    hcl = hcl_regex.search(passport)
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    ecl = ecl_regex.search(passport)
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    pid = pid_regex.search(passport)
    if pid:
        if len(pid.group(1)) == 9 and int(pid.group(1)) < 1000000000:
            pid = True
        else:
            pid = False

    return byr and iyr and eyr and hcl and ecl and pid and hgt


def parse(input: str):
    return input.split("\n\n")
