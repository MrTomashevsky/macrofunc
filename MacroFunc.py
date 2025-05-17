# модуль декларации констант и основных типов данных


from cppLanguageInfo import index
from MyAlg import *

BEGIN_COMMAND = "##"


def CREATE_FUNC_COMMAND(name: str):
    return name + "Command"


# класс названия макрокоманды + список замыкающих ее макрокоманд
# название функции, осуществляющей обработку макрокоманды, можно получить при помощи CREATE_FUNC_COMMAND(<имя макрокоманды>)
class MacroCommand:
    name: str
    endname: list[str]

    def __init__(self, name, endname=[]):
        self.name, self.endname = name, endname


# класс строки с ее номером
class LineString:
    numb: int
    line: str

    def __init__(self, numb: int, line: str):
        self.numb, self.line = numb, line

    def __str__(self):
        spaces = " " * (6 - len(str(self.numb)))
        return f"{self.numb}{spaces}{self.line}"


type TextMacroFunction = list[LineString]
type IndexMacroDirective = tuple[int, int]


IS_NOT_DIRECTIVE: IndexMacroDirective = (-2, -2)
IS_UNKNOWN_DIRECTIVE: IndexMacroDirective = (-1, -1)


# массив существующих директив
listMacroCommand = [
    MacroCommand("macrofunc",
                 ["endmacrofunc"]),
    MacroCommand("integrate"),
    MacroCommand("if",
                 ["elif", "else", "endif"]),
    MacroCommand("elif",
                 ["else", "endif"]),
    MacroCommand("else", ["endif"]),
    MacroCommand("error",),
    MacroCommand("warning",),
    MacroCommand("varline",),
    MacroCommand("varexpr",),
    MacroCommand("foreach",
                 ["endforeach"]),
    MacroCommand("for",
                 ["endfor"])
]


# получить название макрокоманды + ее аргументы (используется при парсинге macrocofunc и integrate)
def getNameAndArgsMacroCommand(line: LineString):
    funcWithArgs = line.line[line.line.index(
        BEGIN_COMMAND)+len(BEGIN_COMMAND)+len(listMacroCommand[indexDirective(line)[0]].name):].strip()

    name = funcWithArgs[:index(funcWithArgs, "(")]
    args = funcWithArgs[index(funcWithArgs, "(") + 1:len(funcWithArgs)-1]

    return name, args


# парсинг строки с целью поиска в ней директивы
# если найдена открывающая директива или просто одиночная директива - возврат
#   tuple(<индекс директивы массиве директив>, -1)
# если найден директива и при этом она существует - возврат
#   tuple(<индекс директивы массиве директив>, <индекс закрывающей директивы в массиве закрывающих директив>)
# если найдена неизвестная директива - возврат IS_UNKNOWN_DIRECTIVE
# не директива - возврат IS_NOT_DIRECTIVE
def indexDirective(line: LineString) -> IndexMacroDirective:
    index: int
    try:
        index = line.line.index(BEGIN_COMMAND)
    except ValueError:
        return IS_NOT_DIRECTIVE

    string = line.line[:index]

    if string.isspace() or len(string) == 0:
        tmpLine = line.line[index+len(BEGIN_COMMAND):]

        for i, j in enumerate(listMacroCommand):
            try:
                if tmpLine.index(j.name) == 0:
                    return (i, -1)
            except ValueError:
                pass
            for ii, jj in enumerate(j.endname):
                try:
                    if tmpLine.index(jj) == 0:
                        return (i, ii)
                except ValueError:
                    pass

        return IS_UNKNOWN_DIRECTIVE
    return IS_NOT_DIRECTIVE


# true если в массиве директив по индексу находится macrofunc
def isIndexBeginMacroFunc(index: IndexMacroDirective) -> bool:
    return index == (0, -1)


# true если в строке находится macrofunc
def isBeginMacroFunc(line: LineString) -> bool:
    return isIndexBeginMacroFunc(indexDirective(line))


# true если в массиве директив по индексу находится endmacrofunc
def isIndexEndMacroFunc(index: IndexMacroDirective) -> bool:
    return index == (0, 0)


# true если в строке находится endmacrofunc
def isEndMacroFunc(line: LineString) -> bool:
    return isIndexEndMacroFunc(indexDirective(line))


# true если в массиве директив по индексу находится integrate
def isIndexIntegrate(index: IndexMacroDirective) -> bool:
    return index == (1, -1)


# true если в строке находится integrate
def isIntegrate(line: LineString) -> bool:
    return isIndexIntegrate(indexDirective(line))


# true если в строке есть директива
def isDirective(line: LineString) -> bool:
    return indexDirective(line) != IS_NOT_DIRECTIVE
