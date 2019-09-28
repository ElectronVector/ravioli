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