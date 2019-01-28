import re
from pprint import pprint

import pycparser
from pycparser import c_ast

from subprocess import check_output


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


def run(filename, include_paths):
    text = preprocess(filename, include_paths)
    text = sanitize(text)
    ast = pycparser.c_parser.CParser().parse(text, filename)

    v = CustomVisitor()
    v.visit(ast)

    for e in ast.ext:
        if type(e) is c_ast.Decl:
            if "static" not in e.storage and "extern" not in e.storage and type(e.type) is not c_ast.FuncDecl:
                v.results['global_count'] += 1

    return v.results


class CustomVisitor(c_ast.NodeVisitor):

    def __init__(self):
        self.results = {'global_count': 0,
                        "complexity": {}
                        }

    def calculate_complexity_if_exists(self, item, attribute):
        complexity = 0
        if hasattr(item, attribute):
            complexity = self.calculate_complexity(getattr(item, attribute, None))
        return complexity

    def calculate_single_item_complexity(self, item):
        complexity = 0

        if type(item) in [c_ast.If, c_ast.While, c_ast.For, c_ast.DoWhile, c_ast.Case]:
            complexity += 1

        complexity += self.calculate_complexity_if_exists(item, 'cond')
        complexity += self.calculate_complexity_if_exists(item, 'stmt')
        complexity += self.calculate_complexity_if_exists(item, 'iftrue')
        complexity += self.calculate_complexity_if_exists(item, 'iffalse')
        complexity += self.calculate_complexity_if_exists(item, 'left')
        complexity += self.calculate_complexity_if_exists(item, 'right')

        if hasattr(item, 'stmts'):
            for stmt in item.stmts:
                complexity += self.calculate_complexity(stmt)

        if type(item) is c_ast.BinaryOp and (item.op == "&&" or item.op == "||"):
            complexity += 1

        return complexity

    def calculate_complexity(self, node):
        complexity = 0
        if type(node) is c_ast.Compound and node.block_items is not None:
            for item in node.block_items:
                complexity += self.calculate_single_item_complexity(item)
        else:
            complexity += self.calculate_single_item_complexity(node)
        return complexity

    def visit_FuncDef(self, node):
        self.results["complexity"][node.decl.name] = self.calculate_complexity(node.body) + 1
        # if node.decl.name == "switch_statement_with_nested_if":
        #     pprint(node)


from pathlib import Path

if __name__ == "__main__":
    folder = Path('./motobox')

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
            pprint(run(str(f), paths))
        except:
            print("   Unable to parse")

    # pprint(run("motobox\Sources\can.c"))
