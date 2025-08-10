import string
import sys
from typing import Callable

# import pyparsing - available if you need it!
# import lark - available if you need it!


def match_count(input_line: str, pattern: str) -> int:
    count = 0
    while count < len(input_line):
        if match_deep(input_line[:count+1], pattern):
            return count + 1
        count += 1
    return 0


def match_pattern_single(input_line: str, pattern: str, match_pattern: str, match_fn: Callable[str, bool]) -> bool:
    len_pattern = len(match_pattern)
    this_match = match_fn(input_line)
    if len(pattern) > len_pattern:
        if pattern[len_pattern] == "+" and len(input_line) > 0:
            next_match = match_deep(input_line[1:], pattern[len_pattern+1:])
            more_match = match_deep(input_line[1:], pattern)
            return (next_match or more_match) and this_match
        if pattern[len_pattern] == "?":
            next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[len_pattern+1:])
            zero_match = match_deep(input_line, pattern[len_pattern+1:])
            return zero_match or (next_match and this_match)
    next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[len_pattern:])
    return next_match and this_match


def match_pattern_set(input_line: str, pattern: str, pattern_head: str, pattern_tail: str, match_fn: Callable[[str, str], bool]) -> bool:
    pattern_end = pattern.find(pattern_tail)
    if pattern_end == -1:
        raise ValueError("invalid pattern")
    pattern_set = pattern[len(pattern_head):pattern_end]
    this_match = match_fn(input_line, pattern_set)
    if len(pattern) > pattern_end + len(pattern_tail):
        if pattern[pattern_end + len(pattern_tail)] == "+" and len(input_line) > 0:
            next_match = match_deep(input_line[1:], pattern[pattern_end + len(pattern_tail) + 1 :])
            more_match = match_deep(input_line[1:], pattern)
            return (next_match or more_match) and this_match
        if pattern[pattern_end + len(pattern_tail)] == "?":
            next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[pattern_end + len(pattern_tail) + 1 :])
            zero_match = match_deep(input_line, pattern[pattern_end + len(pattern_tail) + 1 :])
            return zero_match or (next_match and this_match)
    next_match = len(input_line) > 0 and match_deep(input_line[1:], pattern[pattern_end + len(pattern_tail) :])
    return next_match and this_match


def match_pattern_group(input_line: str, pattern: str, pattern_head: str, pattern_tail: str) -> bool:
    pattern_end = pattern.find(pattern_tail)
    if pattern_end == -1:
        raise ValueError("invalid pattern")
    group_start = len(pattern_head)
    while True:
        next_start = pattern.find(pattern_head, group_start, pattern_end)
        if next_start == -1:
            break
        pattern_end = pattern.find(pattern_tail, pattern_end + len(pattern_tail))
        if pattern_end == -1:
            raise ValueError("invalid pattern")
        group_start = next_start + len(pattern_head)
    pattern_set = pattern[len(pattern_head):pattern_end]
    this_count = match_count(input_line, pattern_set)
    this_match = this_count > 0
    if len(pattern) > pattern_end + len(pattern_tail):
        if pattern[pattern_end + len(pattern_tail)] == "+" and len(input_line) >= this_count:
            next_match = match_deep(input_line[this_count:], pattern[pattern_end + len(pattern_tail) + 1 :])
            more_count = match_count(input_line[this_count:], pattern_set)
            more_match = more_count > 0
            return (next_match or more_match) and this_match
        if pattern[pattern_end + len(pattern_tail)] == "?":
            next_match = len(input_line) >= this_count and match_deep(input_line[this_count:], pattern[pattern_end + len(pattern_tail) + 1 :])
            zero_match = match_deep(input_line, pattern[pattern_end + len(pattern_tail) + 1 :])
            return zero_match or (next_match and this_match)
    next_match = len(input_line) >= this_count and match_deep(input_line[this_count:], pattern[pattern_end + len(pattern_tail) :])
    return next_match and this_match


def match_deep(input_line: str, pattern: str) -> bool:
    if pattern == "":
        return True

    if pattern.startswith("$"):
        if len(pattern) > 1:
            raise ValueError("invalid pattern")
        return len(input_line) == 0

    if pattern.startswith("."):
        return match_pattern_single(input_line, pattern, ".", lambda i: True)

    if pattern.startswith(r"\d"):
        return match_pattern_single(input_line, pattern, r"\d", lambda i: len(i) > 0 and i[0] in string.digits)

    if pattern.startswith(r"\w"):
        return match_pattern_single(input_line, pattern, r"\w", lambda i: len(i) > 0 and i[0] in string.digits + string.ascii_letters + "_")

    if pattern.startswith("[^"):
        return match_pattern_set(input_line, pattern, "[^", "]", lambda i, p: len(i) > 0 and i[0] not in p)

    if pattern.startswith("["):
        return match_pattern_set(input_line, pattern, "[", "]", lambda i, p: len(i) > 0 and i[0] in p)

    if pattern.startswith("("):
        return match_pattern_group(input_line, pattern, "(", ")")

    return match_pattern_single(input_line, pattern, pattern[0], lambda i: len(i) > 0 and i[0] == pattern[0])


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
