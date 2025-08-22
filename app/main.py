import pathlib
import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def split_pattern(pattern):
    splits = []
    level = 0
    for i, c in enumerate(pattern):
        if c == "(":
            level += 1
        elif c == ")":
            level -= 1
        elif c == "|" and level == 0:
            splits.append(i)
    prev = 0
    parts = []
    for s in splits:
        parts.append(pattern[prev:s])
        prev = s + 1
    parts.append(pattern[prev:])
    return parts


def match_plus(input_line, pattern, remaining):
    while len(input_line) > 0 and match_here(input_line[0], pattern):
        input_next = input_line[1:]
        if match_here(input_next, remaining):
            return True
        input_line = input_next
    return False


def match_question(input_line, pattern, remaining):
    input_next = input_line[1:]
    if len(input_line) > 0 and match_here(input_line[0], pattern) and match_here(input_next, remaining):
        return True
    return match_here(input_line, remaining)


def match_group(input_line, pattern):
    pattern_end = pattern.find(")")
    if pattern_end == -1:
        raise ValueError("invalid pattern")
    group_start = 1
    while True:
        next_start = pattern.find("(", group_start)
        if next_start == -1 or next_start > pattern_end:
            break
        pattern_end = pattern.find(")", pattern_end+1)
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        group_start = next_start + 1
    pattern_set = pattern[1:pattern_end]
    pattern_options = split_pattern(pattern_set)
    if len(pattern) > pattern_end+1:
        if pattern[pattern_end+1] == "+":
            remaining = pattern[pattern_end+2:]
            group_count = 0
            while any(match_here(input_line, opt*(group_count+1)) for opt in pattern_options):
                group_count += 1
            if group_count == 0:
                return False
            return any(match_here(input_line, opt*(c+1)+remaining) for opt in pattern_options for c in range(group_count))
        if pattern[pattern_end+1] == "?":
            remaining = pattern[pattern_end+2:]
            return any(match_here(input_line, opt+remaining) for opt in pattern_options) or match_here(input_line, remaining)
    remaining = pattern[pattern_end+1:]
    return any(match_here(input_line, opt+remaining) for opt in pattern_options)


def match_here(input_line, pattern):
    if pattern.startswith("("):
        return match_group(input_line, pattern)
    if pattern == "":
        return True
    if input_line == "":
        return pattern == "$"
    if pattern.startswith(r"\d"):
        if len(pattern) > 2:
            if pattern[2] == "+":
                return match_plus(input_line, r"\d", pattern[3:])
            if pattern[2] == "?":
                return match_question(input_line, r"\d", pattern[3:])
        return (input_line[0] in string.digits) and match_here(input_line[1:], pattern[2:])
    if pattern.startswith(r"\w"):
        if len(pattern) > 2:
            if pattern[2] == "+":
                return match_plus(input_line, r"\w", pattern[3:])
            if pattern[2] == "?":
                return match_question(input_line, r"\w", pattern[3:])
        return (input_line[0] in string.digits + string.ascii_letters + "_") and match_here(input_line[1:], pattern[2:])
    if pattern.startswith("[^"):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[2:pattern_end]
        return (input_line[0] not in pattern_set) and match_here(input_line[2:], pattern[pattern_end+1:])
    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[1:pattern_end]
        return (input_line[0] in pattern_set) and match_here(input_line[1:], pattern[pattern_end+1:])
    if pattern.startswith("."):
        if len(pattern) > 1:
            if pattern[1] == "+":
                return match_plus(input_line, ".", pattern[2:])
            if pattern[1] == "?":
                return match_question(input_line, ".", pattern[2:])
        return match_here(input_line[1:], pattern[1:])
    if len(pattern) > 1:
        if pattern[1] == "+":
            return match_plus(input_line, pattern[0], pattern[2:])
        if pattern[1] == "?":
            return match_question(input_line, pattern[0], pattern[2:])
    return (input_line[0] == pattern[0]) and match_here(input_line[1:], pattern[1:])


def match_pattern(input_line, pattern):
    if pattern.startswith("^"):
        return match_here(input_line, pattern[1:])
    while len(input_line) > 0:
        if match_here(input_line, pattern):
            return True
        input_line = input_line[1:]
    return False


def main():
    recursive = False
    if "-r" in sys.argv:
        recursive = True
        sys.argv.remove("-r")

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    pattern = sys.argv[2]

    if len(sys.argv) < 4:
        input_line = sys.stdin.read()
        if match_pattern(input_line, pattern):
            exit(0)
        exit(1)

    success = False
    input_files = [pathlib.Path(input_path) for input_path in sys.argv[3:]]
    if recursive:
        input_files = [
            fn
            for input_path in input_files
            for fn in input_path.rglob("*")
            if fn.is_file()
        ]
    multi_files = len(input_files) > 1
    for input_file in input_files:
        for input_line in input_file.read_text().split("\n"):
            if match_pattern(input_line, pattern):
                success = True
                print((f"{input_file}:" if multi_files else "") + input_line)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
