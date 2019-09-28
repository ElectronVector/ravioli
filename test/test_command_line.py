import io
import sys
from ravioli.ravioli import main


def run_ravioli():
    """ Run ravioli and capture stdout.
    :return: The stdout captured during execution.
    """
    original_stdout = sys.stdout
    captured_stdout = io.StringIO()
    sys.stdout = captured_stdout
    main()
    sys.stdout = original_stdout
    return captured_stdout.getvalue()


def test_results_for_files():
    sys.argv = ["ravioli", "."]
    stdout = run_ravioli()
    assert ("sample.c" in stdout)
    assert ("main.c" in stdout)


def test_f_option_includes_globals():
    sys.argv = ["ravioli", ".", "-f"]
    stdout = run_ravioli()
    assert ("sample.c:2 global_variable" in stdout)
    assert ("sample.c:3 another_global" in stdout)


def test_x_option_parses_only_c_files():
    sys.argv = ["ravioli", "-x", "c", "."]
    stdout = run_ravioli()
    assert ("sample.c" in stdout)
    assert ("main.c" in stdout)
    assert ("another_file.cpp" not in stdout)


def test_x_option_parses_only_cpp_files():
    sys.argv = ["ravioli", "-x", "cpp", "."]
    stdout = run_ravioli()
    assert ("sample.c" not in stdout)
    assert ("main.c" not in stdout)
    assert ("another_file.cpp" in stdout)


def test_x_option_with_multiple_extensions():
    sys.argv = ["ravioli", "-x", "c", "-x", "cpp", "."]
    stdout = run_ravioli()
    assert ("sample.c" in stdout)
    assert ("main.c" in stdout)
    assert ("another_file.cpp" in stdout)


def test_find_globals_after_initialized_array_in_file():
    sys.argv = ["ravioli", "c/initialized_array.c", "-f"]
    stdout = run_ravioli()
    assert ("initialized_array.c:1 factoryCode" in stdout)
    assert ("initialized_array.c:2 test1" in stdout)
    assert ("initialized_array.c:3 test2" in stdout)