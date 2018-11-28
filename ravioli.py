from pycparser import c_ast, parse_file


def run(filename):
    ast = parse_file(filename, use_cpp=True)
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
        if type(node) is c_ast.Compound:
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


if __name__ == "__main__":
    ast = parse_file("test/c/foo.c", use_cpp=True)
    v = CustomVisitor()
    v.visit(ast)
    ast.show()
