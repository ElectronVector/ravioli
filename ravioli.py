import re
import sys
from pathlib import Path

from subprocess import check_output

import c_parser
from line_counter import LineCounter


def preprocess(filename, include_paths):
    """ Preprocess a file using gcc as the preprocessor.

        filename:
            The name of the file (path to the file) to preprocess.

        include_paths:
            All the paths that files may be included from.

        When successful, returns the contents of the preprocessed file.
        Errors from the processor are printed.
    """
    cpp_path = 'gcc'
    cpp_args = [r'-E', r'-Ifake_libc_include']
    for path in include_paths:
        cpp_args.append(f'-I{path}')

    command = [cpp_path] + cpp_args + [filename]

    try:
        # Note the use of universal_newlines to treat all newlines
        # as \n for Python's purpose
        text = check_output(command, universal_newlines=True)
    except OSError as e:
        raise RuntimeError("Unable to invoke 'cpp'.  " +
                           'Make sure its path was passed correctly\n' +
                           ('Original error: %s' % e))

    return text


def sanitize(text):
    """ Sanitize some C code be removing non-standard compiler extensions.

        text:
            The C code to sanitize.

    """
    text = text.replace('__interrupt', '')
    text = text.replace('interrupt', '')
    text = text.replace('*far', '*')
    matcher = '@(___)'  # An example of what you might use.
    matcher = re.escape(matcher)
    matcher = matcher.replace('___', '.*')
    text = re.sub(matcher, '', text)
    return text


if __name__ == "__main__":
    folder = Path('./motobox')

    if len(sys.argv) > 1:
        folder = Path(sys.argv[1])

    # Find all the source files.
    source_files = list(folder.glob('**/*.c'))

    # Find all the subfolder paths within this directory. We'll pass all of them to preprocessor, so that we
    # most likely can find all of our include files.
    paths = list(folder.glob('**/'))
    paths = [str(path) for path in paths if path.is_dir()]

    print(f"Found {len(source_files)} source files...")

    for f in source_files:
        print(f"   {str(f)}")
        try:
            results = c_parser.parse(str(f), paths)
            loc = LineCounter.count_file(f)
            max_scc = max(results['complexity'].values())
            sf = max_scc + (5*results['global_count']) + (loc/20)
            print(f"SLOC: {loc}, SCC: {max_scc}, Globals: {results['global_count']}, SF: {sf}")
        except:
            print("   Unable to parse")

    # pprint(run("motobox\Sources\can.c"))
