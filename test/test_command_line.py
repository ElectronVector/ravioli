import io
import sys
from ravioli.ravioli import main


def run_and_capture_stdout():
    so = sys.stdout
    capture_stdout = io.StringIO()
    sys.stdout = capture_stdout
    main()
    sys.stdout = so
    return capture_stdout.getvalue()


def test_results_for_files():
    sys.argv = ["ravioli", "."]
    stdout = run_and_capture_stdout()
    assert ("sample.c" in stdout)
    assert ("main.c" in stdout)
