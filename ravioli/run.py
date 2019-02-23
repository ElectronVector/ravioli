import argparse
import sys
import traceback
from pprint import pprint

from pathlib import Path

from ravioli.complexity import calculate_complexity
from ravioli.global_finder import find_globals
from ravioli.line_counter import count


def run(filename):
    print(str(filename))
    try:
        with open(filename, 'r') as f:
            contents = f.read()
            functions = calculate_complexity(contents)
            globals_vars = find_globals(contents)
            loc = count(contents)
            max_scc = max(functions.values())
            print('loc: ' + str(loc))
            print('globals: ' + str(len(globals_vars)))
            print('max scc: ' + str(max_scc))
            ksf = max_scc + (5*len(globals_vars)) + (loc // 10)
            print('ksf: ' + str(ksf))
    except:
        print('*** unable to parse')
        traceback.print_exc(file=sys.stdout)


parser = argparse.ArgumentParser(description='Calculate complexity metrics for C code, specifically the Koopman '
                                             'Spaghetti Factor.')
parser.add_argument('source', help='the source file or folder for which to calculate metrics')
args = parser.parse_args()
run(args.source)

# if __name__ == "__main__":
#     folder = Path('../motobox')
#
#     if len(sys.argv) > 1:
#         folder = Path(sys.argv[1])
#
#     # Find all the source files.
#     source_files = list(folder.glob('**/*.c'))
#
#     # Find all the subfolder paths within this directory. We'll pass all of them to preprocessor, so that we
#     # most likely can find all of our include files.
#     paths = list(folder.glob('**/'))
#     paths = [str(path) for path in paths if path.is_dir()]
#
#     print(f"Found {len(source_files)} source files...")
#
#     for filename in source_files:
#         print(f"{str(filename)}")
#         try:
#             with open(filename, 'r') as f:
#                 #functions = calculate_complexity(f.read())
#                 globals_vars = find_globals(f.read())
#                 pprint(globals_vars)
#         except:
#             print(f'*** unable to parse')
#             traceback.print_exc(file=sys.stdout)
#
#     # for f in source_files:
#     #     print(f"   {str(f)}")
#     #     try:
#     #         results = c_parser.parse(str(f), paths)
#     #         loc = LineCounter.count_file(f)
#     #         max_scc = max(results['complexity'].values())
#     #         sf = max_scc + (5*results['global_count']) + (loc // 20)
#     #         print(f"SLOC: {loc}, SCC: {max_scc}, Globals: {results['global_count']}, SF: {sf}")
#     #     except:
#     #         print("   Unable to parse")

