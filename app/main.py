import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_here(input_line, pattern):
    if pattern == "":
        return True
    if input_line == "":
        return False
    if pattern.startswith(r"\d"):
        return (input_line[0] in string.digits) and match_here(input_line[1:], pattern[2:])
    if pattern.startswith(r"\w"):
        return (input_line[0] in string.digits + string.ascii_letters + "_") and match_here(input_line[1:], pattern[2:])
    if pattern.startswith(r"["):
        pattern_end = pattern.find("]")
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        if pattern[1] == "^":
            return (input_line[0] not in pattern[2:pattern_end]) and match_here(input_line[1:], pattern[pattern_end+1:])
        return (input_line[0] in pattern[1:pattern_end]) and match_here(input_line[1:], pattern[pattern_end+1:])
    return (input_line[0] == pattern[0]) and match_here(input_line[1:], pattern[1:])


def match_pattern(input_line, pattern):
    while len(input_line) > 0:
        if match_here(input_line, pattern):
            return True
        input_line = input_line[1:]
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
