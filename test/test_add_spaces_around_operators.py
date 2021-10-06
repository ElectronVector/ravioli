from ravioli.extract_declarations_and_usages import add_spaces_around_operators


def test_bitshift_and_assignment():
    code = "a<<=1"
    assert add_spaces_around_operators(code) == "a <<= 1"


def test_bitshift_right_and_assignment():
    code = "a>>=1"
    assert add_spaces_around_operators(code) == "a >>= 1"


def test_bitshift():
    code = "a<<1"
    assert add_spaces_around_operators(code) == "a << 1"


def test_less_than():
    code = "a<1"
    assert add_spaces_around_operators(code) == "a < 1"


def test_some_boolean_logic():
    code = "!a||b&&c"
    assert add_spaces_around_operators(code) == " ! a || b && c"


def test_dont_add_spaces_around_dereferencing_stuct_member_access_operator():
    code = "my_struct->value"
    assert add_spaces_around_operators(code) == "my_struct->value"
