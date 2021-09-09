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
    def __init__(self, name, static=False):
        self.name = name
        self.static = static


class VariableExtractor:
    def __init__(self):
        self.declarations = []
        self.usages = []
        self.functions = []

    def _save_token(self, token, type_):
        name_index = 1
        static = False
        # Check for declaration qualifiers.
        if token[0] == "static":
            name_index += 1
            static = True
        type_.append(Token(token[name_index], static))

    def extract_declaration(self, token):
        self._save_token(token, self.declarations)
        print(f"extracting declaration: {token}")

    def extract_assignment(self, token):
        self.usages.append(Token(token[0]))
        print(f"extracting assignment: {token}")

    def extract_function(self, token):
        self._save_token(token, self.functions)
        print(f"extracting function: {token}")

    def extract(self, code):
        type_ = Word(alphanums)
        identifier = Word(alphas, alphanums + "_")
        declaration = Optional(Keyword("static")) + type_ + identifier + Optional("=" + Word(alphanums)) + ";"
        declaration.setParseAction(self.extract_declaration)

        assignment = identifier + "=" + Word(alphanums) + ";"
        assignment.setParseAction(self.extract_assignment)

        function = Optional(Keyword("static")) + type_ + identifier + "(" + ... + ")" + nestedExpr("{", "}")
        function.setParseAction(self.extract_function)

        ZeroOrMore(MatchFirst([assignment, declaration, function])).parseString(code)

        return self

    def get_all_as_dict(self):
        """Get all of the extracted variable information in a single dictionary.
        Note: Call `extract` first to do the extraction.
        :return: A dictionary containing all variable information.
        """
        return {
            "declarations": self.declarations,
            "usages": self.usages,
            "functions": self.functions,
        }


def extract_variables(code):
    return VariableExtractor().extract(code).get_all_as_dict()
