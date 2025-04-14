# модуль обработки комментариев С++

from MyAlg import *


# нахождение индекса открытия многострочного комментария
def indexBeginMultiLineComment(line: str) -> int:
    return index(line, "/*")


# нахождение индекса закрытия многострочного комментария
def indexEndMultiLineComment(line: str) -> int:
    return index(line, "*/")


# нахождение индекса однострочного комментария
def indexSingleLineComment(line: str) -> int:
    return index(line, "//")


# true если в строке нет комментариев
def noComments(line: str) -> bool:
    return indexBeginMultiLineComment(line) == indexEndMultiLineComment(line) == indexSingleLineComment(line) == -1
