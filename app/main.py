import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_deep(input_line, pattern):
    if pattern == "":
        return True

    if pattern.startswith("$"):
        if len(pattern) > 1:
            raise ValueError("invalid pattern")
        return len(input_line) == 0

    if len(input_line) == 0:
        return False

    if pattern.startswith("."):
        this_match = True
        if len(pattern) > 1:
            next_match = match_deep(input_line[1:], pattern[2:])
            if pattern[1] == "+":
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[1] == "?":
                zero_match = match_deep(input_line, pattern[2:])
                return zero_match or (next_match and this_match)
        next_match = match_deep(input_line[1:], pattern[1:])
        return next_match and this_match

    if pattern.startswith(r"\d"):
        this_match = input_line[0] in string.digits
        if len(pattern) > 2:
            next_match = match_deep(input_line[1:], pattern[3:])
            if pattern[2] == "+":
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[2] == "?":
                zero_match = match_deep(input_line, pattern[3:])
                return zero_match or (next_match and this_match)
        next_match = match_deep(input_line[1:], pattern[2:])
        return next_match and this_match

    if pattern.startswith(r"\w"):
        this_match = input_line[0] in string.digits + string.ascii_letters + "_"
        if len(pattern) > 2:
            next_match = match_deep(input_line[1:], pattern[3:])
            if pattern[2] == "+":
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[2] == "?":
                zero_match = match_deep(input_line, pattern[3:])
                return zero_match or (next_match and this_match)
        next_match = match_deep(input_line[1:], pattern[2:])
        return match_deep(input_line[1:], pattern[2:]) and this_match

    if pattern.startswith("[^"):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[2:pattern_end]
        this_match = input_line[0] not in pattern_set
        if len(pattern) > pattern_end+1:
            next_match = match_deep(input_line[1:], pattern[pattern_end+2:])
            if pattern[pattern_end+1] == "+":
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[pattern_end+1] == "?":
                zero_match = match_deep(input_line, pattern[pattern_end+2:])
                return zero_match or (next_match and this_match)
        next_match = match_deep(input_line[1:], pattern[pattern_end+1:])
        return next_match and this_match

    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[2:pattern_end]
        this_match = input_line[0] in pattern_set
        if len(pattern) > pattern_end+1:
            next_match = match_deep(input_line[1:], pattern[pattern_end+2:])
            if pattern[pattern_end+1] == "+":
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[pattern_end+1] == "?":
                zero_match = match_deep(input_line, pattern[pattern_end+2:])
                return zero_match or (next_match and this_match)
        next_match = match_deep(input_line[1:], pattern[pattern_end+1:])
        return next_match and this_match

    this_match = pattern[0] == input_line[0]
    if len(pattern) > 1:
        next_match = match_deep(input_line[1:], pattern[2:])
        if pattern[1] == "+":
            more_match = match_deep(input_line[1:], pattern)
            return (next_match or more_match) and this_match
        if pattern[1] == "?":
            zero_match = match_deep(input_line, pattern[2:])
            return zero_match or (next_match and this_match)
    next_match = match_deep(input_line[1:], pattern[1:])
    return next_match and this_match


def match_pattern(input_line, pattern):
    if pattern[0] == "^":
        return match_deep(input_line, pattern[1:])

    i = 0
    while i < len(input_line):
        if match_deep(input_line[i:], pattern):
            return True
        i += 1

    return False


def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern):
        exit(0)

    exit(1)


if __name__ == "__main__":
    main()
