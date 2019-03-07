import argparse
import os
import sys
import traceback
from operator import itemgetter
from pathlib import Path
from pprint import pprint

from ravioli.complexity import calculate_complexity
from ravioli.global_finder import find_globals
from ravioli.line_counter import count


def run(filename, full_format):
    if full_format:
        report_all_functions(filename)
    else:
        report_ksf_for_all_modules(filename)


def __file_result_is_valid(result):
    return result is not None


def report_all_functions(filename):
    results = []
    if not os.path.isdir(filename):
        # This is a single file.
        results.append(run_single_file(filename))
    else:
        # This is a directory. Run on all the files we can find.
        source_files = list(Path(filename).glob('**/*.c'))

        for f in source_files:
            result = run_single_file(str(f))
            if __file_result_is_valid(result):
                results.append(result)

    # Print globals.
    print("-------------------------------------------------------------------------------")
    print("Globals                                                                        ")
    print("-------------------------------------------------------------------------------")
    for result in results:
        for g in result['globals_vars']:
            print(result['filename'] + ':' + str(g.line_number) + ' ' + g.name)

    # Assemble all the functions into one list.
    functions = []
    for result in results:
        for f in result['functions']:
            functions.append({'filename': result['filename'], 'line_number': f.line_number, 'name': f.name, 'complexity': f.complexity})

    # Sort the functions by complexity.
    functions = sorted(functions, key=itemgetter('complexity'), reverse=True)

    # Print functions.
    print("-------------------------------------------------------------------------------")
    print("Functions                                                            complexity")
    print("-------------------------------------------------------------------------------")
    for f in functions:
        print(f['filename'] + ':' + str(f['line_number']))
        print('     {name:70} {complexity:3}'.format(name=f['name'], complexity=f['complexity']))


def report_ksf_for_all_modules(filename):
    results = []
    if not os.path.isdir(filename):
        # This is a single file.
        results.append(run_single_file(filename))
    else:
        # This is a directory. Run on all the files we can find.
        source_files = list(Path(filename).glob('**/*.c'))

        for f in source_files:
            result = run_single_file(str(f))
            if __file_result_is_valid(result):
                # Only save results that are valid.
                results.append(result)

    # Sort by spaghetti factor.
    results = sorted(results, key=itemgetter('ksf'), reverse=True)

    print("-------------------------------------------------------------------------------")
    print("File                                         complexity   globals   lines   ksf")
    print("-------------------------------------------------------------------------------")
    for result in results:
        if len(result['filename']) <= 50:
            print("{file:50}  {complexity:3}       {globals:3}   {loc:5}   {ksf:3}".format(
                file=result['filename'], complexity=result['max_scc'], globals=len(result['globals_vars']),
                loc=result['loc'], ksf=result['ksf']))
        else:
            print(result['filename'])
            print("{placeholder:50}  {complexity:3}       {globals:3}   {loc:5}   {ksf:3}".format(
                placeholder="", complexity=result['max_scc'], globals=len(result['globals_vars']), loc=result['loc'],
                ksf=result['ksf']))


def run_single_file(filename):
    try:
        with open(filename, 'r') as f:
            contents = f.read()
            functions = calculate_complexity(contents)
            globals_vars = find_globals(contents)
            loc = count(contents)
            # Find the maximum complexity (scc) of all functions.
            max_scc = find_max_complexity(functions)
            # Calculate the spaghetti factor.
            ksf = max_scc + (5 * len(globals_vars)) + (loc // 20)
            return {'filename': filename, 'functions': functions, 'max_scc': max_scc, 'globals_vars': globals_vars,
                    'loc': loc, 'ksf': ksf}
    except:
        print('*** unable to parse ({file})'.format(file=filename))
        traceback.print_exc(file=sys.stdout)


def find_max_complexity(functions):
    if len(functions) > 0:
        max_scc = max([f.complexity for f in functions])
    else:
        max_scc = 0
    return max_scc


def main():
    parser = argparse.ArgumentParser(description='Calculate complexity metrics for C code, specifically the Koopman '
                                                 'Spaghetti Factor (KSF).')
    parser.add_argument('source', help='the source file or folder for which to calculate metrics')
    parser.add_argument('-f', action='store_true', help='output a complete list of all globals and functions sorted by complexity')
    args = parser.parse_args()
    run(args.source, args.f)


if __name__ == "__main__":
    main()

