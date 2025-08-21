import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_here(input_line, pattern):
    if pattern.startswith(r"\d"):
        return input_line[0] in string.digits
    if pattern.startswith(r"\w"):
        return input_line[0] in string.digits + string.ascii_letters + "_"
    if len(pattern) == 1:
        return pattern in input_line[0]
    return False


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
