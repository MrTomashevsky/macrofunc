# модуль обработки комментариев и других средств С++

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


# переменная хранит информацию об текущих допусчтимых объявлениях литералов строк
permissibleStringLiterals: list[str] = {
    "L"
}


# true если аргумент является с-строкой
def is_cstr(var: str, permissibleStringLiterals: list[str]):
    var = var.strip()
    return var[-1] == "\"" and (var[0] == "\"" or True in [index(var, i) == 0 and var[len(i)] == "\"" for i in permissibleStringLiterals])
