import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_pattern(input_line, pattern):
    if len(pattern) == 1:
        return pattern in input_line

    if pattern == r"\d":
        return any(c in input_line for c in string.digits)

    if pattern == r"\w":
        return any(c in input_line for c in string.digits + string.ascii_letters + "_")

    if pattern[0] == "[" and pattern[-1] == "]":
        if pattern[1] != "^":
            return any(c in input_line for c in pattern[1:-1])
        return not all(c in input_line for c in pattern[2:-1])

    raise RuntimeError(f"Unhandled pattern: {pattern}")


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
