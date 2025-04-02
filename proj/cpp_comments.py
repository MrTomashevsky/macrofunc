
def index(line, what):
    try:
        return line.index(what)
    except ValueError:
        return -1


def indexBeginMultiLineComment(line):
    return index(line, "/*")


def indexEndMultiLineComment(line):
    return index(line, "*/")


def indexSingleLineComment(line):
    return index(line, "//")


def noComments(line):
    return indexBeginMultiLineComment(line) == indexEndMultiLineComment(line) == indexSingleLineComment(line) == -1
