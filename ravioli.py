import glob
import re
from pprint import pprint

import pycparser
from pycparser import c_ast, parse_file

from subprocess import check_output


def preprocess(filename):
    """ Preprocess a file using gcc as the preprocessor.

        filename:
            The name of the file (path to the file) to preprocess.

        When successful, returns the contents of the preprocessed file.
        Errors from the processor are printed.
    """
    cpp_path = 'gcc'
    cpp_args = [r'-E', r'-Ifake_libc_include', r'-Imotobox', r'-Imotobox/Sources',
                r'-Imotobox/Sources/FreeRTOS/include', r'-Imotobox/Sources/FreeRTOS/portable/CodeWarrior/HCS12']

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


def run(filename):
    text = preprocess(filename)
    text = sanitize(text)
    ast = pycparser.c_parser.CParser().parse(text, filename)
    v = CustomVisitor()
    v.visit(ast)
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

    def visit_Decl(self, node):
        if type(node.type) is c_ast.TypeDecl:
            # A declaration that is not static and not an extern is a global variable.
            if "static" not in node.storage and "extern" not in node.storage:
                self.results['global_count'] += 1


from pathlib import Path

if __name__ == "__main__":
    folder = Path('./motobox')

    source_files = list(folder.glob('**/*.c'))

    print(f"Found {len(source_files)} source files...")

    for f in source_files:
        print(f"   {str(f)}")
        try:
            pprint(run(str(f)))
        except:
            print("   Unable to parse")

    # pprint(run("motobox\Sources\can.c"))
