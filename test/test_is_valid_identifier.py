from ravioli.extract_declarations_and_usages import is_valid_identifier


def test_all_alphas_is_valid():
    assert is_valid_identifier("name")


def test_alphas_and_underscore_is_valid():
    assert is_valid_identifier("a_name")


def test_starting_with_underscore_is_valid():
    assert is_valid_identifier("_a_name")


def test_starting_with_number_is_invalid():
    assert not is_valid_identifier("1invalidname")


def test_number_not_at_start_is_valid():
    assert is_valid_identifier("name1")


def test_a_single_letter_is_valid():
    assert is_valid_identifier("a")


def test_a_single_number_is_invalid():
    assert not is_valid_identifier("1")