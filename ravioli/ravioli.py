import argparse
import os
import traceback
from operator import itemgetter
from pathlib import Path

from ravioli.complexity import calculate_complexity
from ravioli.global_finder import find_globals
from ravioli.line_counter import count


def run(filename, args):
    errors, results = process_files(args, filename)

    if args.f:
        report_all_functions(results, errors, args)
    else:
        report_ksf_for_all_modules(results, errors, args)


def process_files(args, filename):
    results = []
    errors = []
    if not os.path.isdir(filename) and not args.i
        # This is a single file.
        results.append(run_single_file(filename))
    else:
        if args.i:
            source_files = read_source_files_from_file(args)
        else:
            # This is a directory. Run on all the files we can find.
            source_files = get_source_files(args)

        for f in source_files:
            result = run_single_file(str(f))
            if __file_result_is_valid(result):
                # Only save results that are valid.
                results.append(result)
            if type(result) is ParsingError:
                errors.append(result)
    return errors, results


def report_all_functions(results, errors, args):

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
            functions.append({'filename': result['filename'], 'line_number': f.line_number, 'name': f.name,
                              'complexity': f.complexity})

    # Sort the functions by complexity.
    functions = sorted(functions, key=itemgetter('complexity'), reverse=True)

    # Only display results above a threshold.
    functions = [f for f in functions if f['complexity'] >= args.t]

    # Print functions.
    print("-------------------------------------------------------------------------------")
    print("Functions                                                            complexity")
    print("-------------------------------------------------------------------------------")
    for f in functions:
        remaining_filename = __print_wrapped_and_indented_string(f['filename'], 72)
        print(remaining_filename + ':' + str(f['line_number']))

        # Wrap long function names.
        print("    ", end='')
        remaining_function_name = __print_wrapped_and_indented_string(f['name'], 70)
        print('{name:70} {complexity:3}'.format(name=remaining_function_name, complexity=f['complexity']))

    if args.e:
        print("-------------------------------------------------------------------------------")
        print("Errors                                                                         ")
        print("-------------------------------------------------------------------------------")
        for e in errors:
            print("*** ERROR PROCESSING: " + e.filename)
            print(e.message)


def report_ksf_for_all_modules(results, errors, args):

    # Sort by spaghetti factor.
    results = sorted(results, key=itemgetter('ksf'), reverse=True)

    # Only display results above a threshold.
    results = [r for r in results if r['ksf'] >= args.t]

    print("-------------------------------------------------------------------------------")
    print("File                                         complexity   globals   lines   ksf")
    print("-------------------------------------------------------------------------------")
    for result in results:
        remaining_filename = __print_wrapped_and_indented_string(result['filename'], 50)
        if remaining_filename != result['filename']:
            # Some of the filename has already been printed.
            print("{file:46}  {complexity:3}       {globals:3}   {loc:5}   {ksf:3}".format(
                file=remaining_filename, complexity=result['max_scc'], globals=len(result['globals_vars']),
                loc=result['loc'], ksf=result['ksf']))
        else:
            print("{file:50}  {complexity:3}       {globals:3}   {loc:5}   {ksf:3}".format(
                file=remaining_filename, complexity=result['max_scc'], globals=len(result['globals_vars']),
                loc=result['loc'], ksf=result['ksf']))

    if args.e:
        print("-------------------------------------------------------------------------------")
        print("Errors                                                                         ")
        print("-------------------------------------------------------------------------------")
        for e in errors:
            print("*** ERROR PROCESSING: " + e.filename)
            print(e.message)


class ParsingError:
    def __init__(self, filename, message):
        self.filename = filename
        self.message = message


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
        # There was an error parsing this file.
        return ParsingError(filename, traceback.format_exc())


def find_max_complexity(functions):
    if len(functions) > 0:
        max_scc = max([f.complexity for f in functions])
    else:
        max_scc = 0
    return max_scc

def read_source_files_from_file(args):
    with open(args.source,'r') as fh:
        source_files = []
        for line in fh:
            source_files.append(line.strip('\n'))
        return source_files

def get_source_files(args):
    source_files = list(Path(args.source).glob('**/*.c'))
    if args.x is not None:
        source_files = []
        for ext in args.x:
            source_files += list(Path(args.source).glob('**/*.' + str(ext)))
    return source_files


def main():
    parser = argparse.ArgumentParser(description='Calculate complexity metrics for C code, specifically the Koopman '
                                                 'Spaghetti Factor (KSF).')
    parser.add_argument('source', help='the source file or folder for which to calculate metrics')
    parser.add_argument('-f', action='store_true', help='output a complete list of all globals and functions sorted '
                                                        'by complexity')
    parser.add_argument('-t', default=0, type=int, metavar='threshold', help='Only display results at or above this '
                                                                             'threshold (KSF or function complexity)')
    parser.add_argument('-e', action='store_true', help='show any errors encountered processing source files')
    parser.add_argument('-x', action='append', required=False, help='File extensions to include in the analysis (-x c -x cc -x h ...). If omitted, only .c files are analyzed')
    parser.add_argument('-i', action='store_true', help='File with list of files that should be processed')


    args = parser.parse_args()
    run(args.source, args)


def __file_result_is_valid(result):
    return type(result) is not ParsingError


def __print_wrapped_and_indented_string(str, width):
    remaining_str = str
    space_for_str = width
    while len(remaining_str) > space_for_str:
        if len(remaining_str) == len(str):
            # This is the first line.
            print(remaining_str[:space_for_str])
            remaining_str = remaining_str[space_for_str:]
            space_for_str = width - 4
        else:
            print("    ", end='')
            print(remaining_str[:space_for_str])
            remaining_str = remaining_str[space_for_str:]
    if remaining_str != str:
        # We wrapped some of the string. Print an indent so that the next
        # print is indented.
        print("    ", end='')
    return remaining_str


if __name__ == "__main__":
    main()
