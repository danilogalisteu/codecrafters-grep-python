import string
import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_here(pattern, input_line):
    if pattern.startswith(r"\d"):
        return any(input_line[0].startswith(c) for c in string.digits), pattern[2:], input_line[1:]

    if pattern.startswith(r"\w"):
        return any(
            input_line.startswith(c)
            for c in string.digits + string.ascii_letters + "_"
        ), pattern[2:], input_line[1:]

    if pattern.startswith("[^"):
        pattern_end = pattern.find("]")
        pattern_set = pattern[2:pattern_end]
        return not any(
            input_line.startswith(c) for c in pattern_set
        ), pattern[pattern_end + 1 :], input_line[1:]

    if pattern.startswith("["):
        pattern_end = pattern.find("]")
        pattern_set = pattern[1:pattern_end]
        return any(
            input_line.startswith(c) for c in pattern_set
        ), pattern[pattern_end + 1 :], input_line[1:]

    if pattern == "$":
        return input_line == "", pattern[1:], input_line

    if len(pattern) > 0 and len(input_line) > 0:
        return pattern[0] == input_line[0], pattern[1:], input_line[1:]

    return len(pattern) == 0, pattern, input_line


def match_pattern(input_line, pattern):
    if pattern[0] == "^":
        return match_here(pattern[1:], input_line)[0]

    i = 0
    while i < len(input_line):
        prev_input = input_line[i:]
        prev_pattern = pattern
        while prev_pattern:
            is_match, next_pattern, next_input = match_here(prev_pattern, prev_input)
            if not is_match:
                break
            prev_pattern, prev_input = next_pattern, next_input
        i += 1
        if not prev_input and prev_pattern:
            continue
        if is_match:
            return True
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
