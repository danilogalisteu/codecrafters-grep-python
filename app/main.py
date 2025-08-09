import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_count(input_line: str, pattern: str) -> int:
    count = 0
    while count < len(input_line):
        if match_deep(input_line[:count+1], pattern):
            return count + 1
        count += 1
    return 0


def match_wildcard(input_line: str, pattern: str) -> bool:
    this_match = True
    if len(pattern) > 1:
        if pattern[1] == "+" and len(input_line) > 0:
            next_match = match_deep(input_line[1:], pattern[2:])
            more_match = match_deep(input_line[1:], pattern)
            return (next_match or more_match) and this_match
        if pattern[1] == "?":
            next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[2:])
            zero_match = match_deep(input_line, pattern[2:])
            return zero_match or (next_match and this_match)
    next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[1:])
    return next_match and this_match


def match_digit(input_line: str, pattern: str) -> bool:
    this_match = len(input_line) > 0 and input_line[0] in string.digits
    if len(pattern) > 2:
        if pattern[2] == "+" and len(input_line) > 0:
            next_match = match_deep(input_line[1:], pattern[3:])
            more_match = match_deep(input_line[1:], pattern)
            return (next_match or more_match) and this_match
        if pattern[2] == "?":
            next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[3:])
            zero_match = match_deep(input_line, pattern[3:])
            return zero_match or (next_match and this_match)
    next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[2:])
    return next_match and this_match


def match_deep(input_line: str, pattern: str) -> bool:
    if pattern == "":
        return True

    if pattern.startswith("$"):
        if len(pattern) > 1:
            raise ValueError("invalid pattern")
        return len(input_line) == 0

    if pattern.startswith("."):
        return match_wildcard(input_line, pattern)

    if pattern.startswith(r"\d"):
        return match_digit(input_line, pattern)

    if pattern.startswith(r"\w"):
        this_match = len(input_line) > 0 and input_line[0] in string.digits + string.ascii_letters + "_"
        if len(pattern) > 2:
            if pattern[2] == "+" and len(input_line) > 0:
                next_match = match_deep(input_line[1:], pattern[3:])
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[2] == "?":
                next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[3:])
                zero_match = match_deep(input_line, pattern[3:])
                return zero_match or (next_match and this_match)
        next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[2:])
        return next_match and this_match

    if pattern.startswith("[^"):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[2:pattern_end]
        this_match = len(input_line) > 0 and input_line[0] not in pattern_set
        if len(pattern) > pattern_end + 1:
            if pattern[pattern_end + 1] == "+" and len(input_line) > 0:
                next_match = match_deep(input_line[1:], pattern[pattern_end + 2 :])
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[pattern_end + 1] == "?":
                next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[pattern_end + 2 :])
                zero_match = match_deep(input_line, pattern[pattern_end + 2 :])
                return zero_match or (next_match and this_match)
        next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[pattern_end + 1 :])
        return next_match and this_match

    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[1:pattern_end]
        this_match = len(input_line) > 0 and input_line[0] in pattern_set
        if len(pattern) > pattern_end + 1:
            if pattern[pattern_end + 1] == "+" and len(input_line) > 0:
                next_match = match_deep(input_line[1:], pattern[pattern_end + 2 :])
                more_match = match_deep(input_line[1:], pattern)
                return (next_match or more_match) and this_match
            if pattern[pattern_end + 1] == "?":
                next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[pattern_end + 2 :])
                zero_match = match_deep(input_line, pattern[pattern_end + 2 :])
                return zero_match or (next_match and this_match)
        next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[pattern_end + 1 :])
        return next_match and this_match


    if pattern.startswith("("):
        pattern_end = pattern.find(")")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        group_start = 1
        while True:
            next_start = pattern.find("(", group_start, pattern_end)
            if next_start == -1:
                break
            pattern_end = pattern.find(")", pattern_end + 1)
            if pattern_end == -1:
                raise ValueError("invalid pattern")
            group_start = next_start + 1

        pattern_set = pattern[1:pattern_end]
        this_count = match_count(input_line, pattern_set)
        this_match = this_count > 0
        if len(pattern) > pattern_end + 1:
            if pattern[pattern_end + 1] == "+" and len(input_line) >= this_count:
                next_match = match_deep(input_line[this_count:], pattern[pattern_end + 2 :])
                more_count = match_count(input_line[this_count:], pattern_set)
                more_match = more_count > 0
                return (next_match or more_match) and this_match
            if pattern[pattern_end + 1] == "?":
                next_match = len(input_line) >= this_count and match_deep(input_line[this_count:], pattern[pattern_end + 2 :])
                zero_match = match_deep(input_line, pattern[pattern_end + 2 :])
                return zero_match or (next_match and this_match)
        next_match = len(input_line) >= this_count and match_deep(input_line[this_count:], pattern[pattern_end + 1 :])
        return next_match and this_match

    this_match = len(input_line) > 0 and pattern[0] == input_line[0]
    if len(pattern) > 1:
        if pattern[1] == "+" and len(input_line) > 0:
            next_match = match_deep(input_line[1:], pattern[2:])
            more_match = match_deep(input_line[1:], pattern)
            return (next_match or more_match) and this_match
        if pattern[1] == "?":
            next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[2:])
            zero_match = match_deep(input_line, pattern[2:])
            return zero_match or (next_match and this_match)
    next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[1:])
    return next_match and this_match


def match_pattern(input_line: str, pattern: str) -> bool:
    if pattern[0] == "^":
        return match_deep(input_line, pattern[1:])

    i = 0
    while i < len(input_line):
        if match_deep(input_line[i:], pattern):
            return True
        i += 1

    return False


def main() -> None:
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if match_pattern(input_line, pattern):
        print(f"MATCHED\n{pattern}\n{input_line}")
        exit(0)

    print(f"NOT MATCHED\n{pattern}\n{input_line}")
    exit(1)


if __name__ == "__main__":
    main()
