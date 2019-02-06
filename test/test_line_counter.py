from ravioli.line_counter import LineCounter


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


def test_count_lines_with_trailing_comments():
    code = """int i = 0;
              bool x = true; // a comment
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 3)


def test_dont_count_single_line_block_comments():
    code = """int i = 0;
              /* a comment */
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 2)


def test_dont_count_block_comments_spanning_two_lines():
    code = """int i = 0;
              /* a comment
              that spans two lines */
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 2)


def test_dont_count_block_comments_spanning_multiple_lines():
    code = """int i = 0;
              /* a comment
              that spans
              three lines */
              int j = 1;"""
    line_count = LineCounter.count(code)
    assert(line_count == 2)


def test_count_lines_in_a_file():
    line_count = LineCounter.count_file('c/main.c')
    assert(line_count == 6)


def test_count_lines_in_another_file():
    line_count = LineCounter.count_file('c/sample.c')
    assert(line_count == 247)
