import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_deep(input_line, pattern):
    if pattern == "":
        return True

    if pattern.startswith(r"\d"):
        return match_deep(input_line[1:], pattern[2:]) and input_line[0] in string.digits

    if pattern.startswith(r"\w"):
        return match_deep(input_line[1:], pattern[2:]) and input_line[0] in string.digits + string.ascii_letters + "_"

    if pattern.startswith("[^"):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[2:pattern_end]
        return match_deep(input_line[1:], pattern[pattern_end+1:]) and input_line[0] not in pattern_set

    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        pattern_set = pattern[2:pattern_end]
        return match_deep(input_line[1:], pattern[pattern_end+1:]) and input_line[0] in pattern_set

    if pattern.startswith("$"):
        if len(pattern) > 1:
            raise ValueError("invalid pattern")
        return len(input_line) == 0

    if len(input_line) > 0:
        return match_deep(input_line[1:], pattern[1:]) and pattern[0] == input_line[0]

    return False


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
