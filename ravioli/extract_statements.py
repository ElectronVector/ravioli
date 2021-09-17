
class Block:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f"Block({self.title})"

    def __eq__(self, other):
        return self.title == other.title


def extract_statements(code):
    statements = []
    current_statement = ""
    for c in code:
        if c == ";":
            # Save the current statement.
            statements.append(clean_up_whitespace(current_statement))
            current_statement = ""
        elif c == "{":
            title = clean_up_whitespace(current_statement)
            title = title.replace("(", "")
            title = title.replace(")", "")
            statements.append(Block(title))
        else:
            current_statement += c

    return statements


def clean_up_whitespace(s):
    return " ".join(s.strip().split())