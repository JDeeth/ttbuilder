import string


def xml_escape(text: str) -> str:
    """To match style observed in SimSig native XML files"""
    escape = {
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
        "'": "&apos;",
        '"': "&quot;",
    }

    def escape_chr(c):
        if c in escape:
            return escape[c]
        elif ord(c) > 127:
            return f"&#x{ord(c):04X};"
        else:
            return c

    return "".join(escape_chr(c) for c in text)


def pascal_case(snakecase: str):
    """Turns snake_case into PascalCase"""
    return string.capwords(snakecase, sep="_").replace("_", "")
