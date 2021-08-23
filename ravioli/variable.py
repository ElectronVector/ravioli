class Variable:
    def __init__(self, name, line_number=None):
        self.name = name
        self.line_number = line_number

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'Variable("{self.name}", line_number={self.line_number})'
