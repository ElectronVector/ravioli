from pyparsing import (
    Word,
    alphas,
    alphanums,
    Optional,
    delimitedList,
    lineno,
    Keyword, nestedExpr, MatchFirst, printables, ZeroOrMore,
)


class Token:
    def __init__(self, name):
        self.name = name


class VariableExtractor:
    def __init__(self):
        self.declarations = []
        self.usages = []
        self.functions = []

    def extract_declaration(self, token):
        self.declarations.append(Token(token[1]))
        print(f"extracting declaration: {token}")

    def extract_assignment(self, token):
        self.usages.append(Token(token[0]))
        print(f"extracting assignment: {token}")

    def extract_function(self, token):
        self.functions.append(Token(token[1]))
        print(f"extracting function: {token}")

    def extract(self, code):
        type_ = Word(alphanums)
        variable_name = Word(alphas, alphanums + "_")
        declaration = type_ + variable_name + ";"
        declaration.setParseAction(self.extract_declaration)

        assignment = variable_name + "=" + Word(alphanums) + ";"
        assignment.setParseAction(self.extract_assignment)

        function = type_ + variable_name + "(" + ... + ")" + nestedExpr("{", "}")
        function.setParseAction(self.extract_function)

        ZeroOrMore(MatchFirst([assignment, declaration, function])).parseString(code)

        return self

    # Get all of the extracted stuff in a single dictionary.
    def get_all_as_dict(self):
        return {
            "declarations": self.declarations,
            "usages": self.usages,
            "functions": self.functions,
        }


def extract_variables(code):
    return VariableExtractor().extract(code).get_all_as_dict()
