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
    def __init__(self, name, static=False, const=False):
        self.name = name
        self.static = static
        self.const = const


class VariableExtractor:
    def __init__(self):
        self.declarations = []
        self.usages = []
        self.functions = []

    @staticmethod
    def _save_token(parsed_token, type_):
        name_index = 1
        qualifiers = {"static": False, "const": False}
        # Check for declaration qualifiers.
        for i in range(2):
            if parsed_token[i] in ["static", "const"]:
                name_index += 1
                qualifiers[parsed_token[i]] = True
        type_.append(Token(parsed_token[name_index], qualifiers["static"], qualifiers["const"]))

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
        assignment = "=" + Word(alphanums)

        variable_qualifiers = Keyword("static") | Keyword("const")
        declaration = ZeroOrMore(variable_qualifiers) + type_ + identifier + Optional(assignment) + ";"
        declaration.setParseAction(self.extract_declaration)

        variable_assignment = identifier + assignment + ";"
        variable_assignment.setParseAction(self.extract_assignment)

        function_qualifiers = Keyword("static")
        function = ZeroOrMore(function_qualifiers) + type_ + identifier + "(" + ... + ")" + nestedExpr("{", "}")
        function.setParseAction(self.extract_function)

        ZeroOrMore(MatchFirst([variable_assignment, declaration, function])).parseString(code)

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
