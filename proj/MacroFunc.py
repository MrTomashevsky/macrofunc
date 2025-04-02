from cpp_comments import index
from getArgs import *

BEGIN_COMMAND = "##"


class MacroCommand:
    name: str
    endname: list[str]

    def __init__(self, name, endname=[]):
        self.name, self.endname = name, endname


class LineString:
    numb: int
    line: str

    def __init__(self, numb: int, line: str):
        self.numb, self.line = numb, line

    def __str__(self):
        spaces = " " * (6 - len(str(self.numb)))
        return f"{self.numb}{spaces}{self.line}"


type UnprocessedTextOfMacroFunction = list[LineString]

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
    MacroCommand("var",),
    MacroCommand("for",
                 ["endfor"]),
    MacroCommand("foreach",
                 ["endforeach"])
]


def getNameAndArgsMacroCommand(line: LineString):
    funcWithArgs = line.line[line.line.index(
        BEGIN_COMMAND)+len(BEGIN_COMMAND)+len(listMacroCommand[indexDirective(line)[0]].name):].strip()

    name = funcWithArgs[:index(funcWithArgs, "(")]
    args = funcWithArgs[index(funcWithArgs, "(") + 1:len(funcWithArgs)-1]

    return name, args


def indexDirective(line: LineString) -> tuple[int, int]:
    index: int
    try:
        index = line.line.index(BEGIN_COMMAND)
    except ValueError:
        return (-1, -1)

    string = line.line[:index]
    assert not string.isspace() or len(string) != 0, f"\"{string}\""

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

    return (-1, -1)


def isDirective(line: LineString) -> bool:
    return indexDirective(line) != (-1, -1)


def isBeginMacroFunc(line: LineString) -> bool:
    return indexDirective(line) == (0, -1)


def isEndMacroFunc(line: LineString):
    return indexDirective(line) == (0, 0)

    # def processing(line: LineString) -> tuple[int, list[str]]:
    #     pass


def isIntegrate(line: LineString):
    return indexDirective(line) == (1, -1)


# def execute(obj: MacroFunction, args, foutLines: list[str]):
#     variables = {obj.args[i]: args[i] for i in range(len(args))}

#     for i in obj.tail:
#         ind = indexDirective(i)
#         if ind[0] != -1:
#             name: str
#             if ind[1] != -1:
#                 name = listMacroCommand[ind[0]].endname[ind[1]]
#             else:
#                 name = listMacroCommand[ind[0]]

#             globals()[CREATE_FUNC_COMMAND(name)]()
#             break

# macroFunctions: ListMacroFunctionsk,
def integrate(line: LineString, foutLines: list[str]):
    name, args = getNameAndArgsMacroCommand(line)

    global x
    x.add_row([name + "(" + args + ")", name + str(getArgs(args))])

    # find = False
    # for i in macroFunctions:
    #     if i.name == name and len(i.args) == len(args):
    #         find = True
    #         execute(i, args, foutLines)
    #         break

    # assert find

    foutLines.append("has been integrated")
