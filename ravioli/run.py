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


def run(filename):
    print("-------------------------------------------------------------------------------")
    print("File                                         complexity   globals   lines   ksf")
    print("-------------------------------------------------------------------------------")
    results = []
    if not os.path.isdir(filename):
        # This is a single file.
        results.append(run_single_file(filename))
    else:
        # This is a directory. Run on all the files we can find.
        source_files = list(Path(filename).glob('**/*.c'))

        for f in source_files:
            results.append(run_single_file(str(f)))

    # Sort by spaghetti factor.
    results = sorted(results, key=itemgetter('ksf'), reverse=True)

    for result in results:
        if len(result['filename']) <= 50:
            print("{file:50}  {complexity:3}       {globals:3}   {loc:5}   {ksf:3}".format(
                file=result['filename'], complexity=result['max_scc'], globals=len(result['globals_vars']), loc=result['loc'], ksf=result['ksf']))
        else:
            print(result['filename'])
            print("{placeholder:50}  {complexity:3}       {globals:3}   {loc:5}   {ksf:3}".format(
                placeholder="", complexity=result['max_scc'], globals=len(result['globals_vars']), loc=result['loc'], ksf=result['ksf']))


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
            return {'filename': filename, 'max_scc': max_scc, 'globals_vars': globals_vars, 'loc': loc, 'ksf': ksf}
    except:
        print('*** unable to parse ({file})'.format(file=filename))
        traceback.print_exc(file=sys.stdout)


def find_max_complexity(functions):
    if len(functions) > 0:
        max_scc = max(functions.values())
    else:
        max_scc = 0
    return max_scc


parser = argparse.ArgumentParser(description='Calculate complexity metrics for C code, specifically the Koopman '
                                             'Spaghetti Factor.')
parser.add_argument('source', help='the source file or folder for which to calculate metrics')
args = parser.parse_args()
run(args.source)

