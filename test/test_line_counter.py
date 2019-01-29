import pytest


class LineCounter:
    @staticmethod
    def count(string):
        lines = string.splitlines()
        # Remove blank lines.
        lines = [l for l in lines if not l.isspace()]
        # Remove comment lines.
        lines = [l for l in lines if not l.lstrip().startswith("//")]
        return len(lines)


def test_single_line():
    code = "int i = 0;"
    line_count = LineCounter.count(code)
    assert(line_count == 1)


def test_multiple_lines():
    code = """int i = 0;
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 2)


def test_dont_count_blank_lines():
    code = """int i = 0;
    
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 2)


def test_dont_count_comment_lines():
    code = """int i = 0;
              // a comment
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 2)

