import re
import cpp_comments
from cpp_comments import index
from prettytable import PrettyTable


def CREATE_FUNC_COMMAND(name: str):
    return name + "Command"


class MacroFunc:
    pass


class MacroCommand:
    name: str
    endname: list[str]
    regex: str

    def __init__(self, name, regex, endname=[]):
        self.name, self.endname, self.regex = name, endname, regex


class LineString:
    numb: int
    line: str

    def __init__(self, numb: int, line: str):
        self.numb, self.line = numb, line

    def __str__(self):
        spaces = " " * (6 - len(str(self.numb)))
        return f"{self.numb}{spaces}{self.line}"


class MacroFunction:
    name = ""
    args = []

    tail: list[LineString]

    def header(self) -> str:
        return self.name + str(self.args)

    def __init__(self, tail):
        self.tail = tail

    def finalInit(self, macroFunc: MacroFunc):
        def createHeader():
            line = self.tail[0]
            self.name, args = macroFunc.getNameAndArgsMacroCommand(line)
            self.args = getArgs(args)

        def deleteComments():
            tail = []
            isMultiLineComment = False
            ind: int
            for i in self.tail:
                line = i.line

                if isMultiLineComment:
                    ind = cpp_comments.indexEndMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = False
                        line = line[ind+2:]
                    else:
                        line = ""
                else:
                    ind = cpp_comments.indexBeginMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = True
                        line = line[:ind]

                ind = cpp_comments.indexSingleLineComment(i.line)
                if ind != -1:
                    line = line[:ind]

                tail.append(LineString(i.numb, line))

            self.tail = tail

        deleteComments()
        createHeader()


class RegExString:
    TWO_ARGS_IN_SK = "(\\w, \\w)"
    FUNC_WITH_ARGS = "\\s\\w" + "(\\w,* \\w)"
    EXPR = ""
    S_EXPR = ""
    FOR = "(\\w,\\s\\w,\\s\\w,\\s\\w)"


class MacroFunc:

    def getNameAndArgsMacroCommand(self, line: LineString):
        funcWithArgs = line.line[line.line.index(
            "##")+2+len(self.listMacroCommand[self.indexDirective(line)[0]].name):].strip()

        name = funcWithArgs[:index(funcWithArgs, "(")]
        args = funcWithArgs[index(funcWithArgs, "(") + 1:len(funcWithArgs)-1]

        return name, args

    def __str__(self):
        returnValue = ""
        for i, obj in enumerate(self.macroFunctions):

            returnValue = returnValue + "\033[35m" + str(i) + "\033[0m\n"
            for j in obj.tail:
                returnValue = returnValue + str(j)
        return returnValue

    listMacroCommand = [
        MacroCommand("macrofunc",
                     RegExString.FUNC_WITH_ARGS,
                     ["endmacrofunc"]),
        MacroCommand("integrate",
                     RegExString.FUNC_WITH_ARGS),
        MacroCommand("if",
                     RegExString.EXPR,
                     ["elif", "else", "endif"]),
        MacroCommand("elif",
                     RegExString.EXPR,
                     ["else", "endif"]),
        MacroCommand("else", ["endif"]),
        MacroCommand("error",
                     RegExString.S_EXPR),
        MacroCommand("warning",
                     RegExString.S_EXPR),
        MacroCommand("var",
                     RegExString.TWO_ARGS_IN_SK),
        MacroCommand("for",
                     RegExString.FOR,
                     ["endfor"]),
        MacroCommand("foreach",
                     RegExString.TWO_ARGS_IN_SK,
                     ["endforeach"])
    ]

    macroFunctions: list[MacroFunction] = []

    def indexDirective(self, line: LineString) -> tuple[int, int]:
        index: int
        try:
            index = line.line.index("##")
        except ValueError:
            return (-1, -1)

        string = line.line[:index]
        assert not string.isspace() or len(string) != 0, f"\"{string}\""

        tmpLine = line.line[index+2:]
        for i, j in enumerate(self.listMacroCommand):
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

    def isDirective(self, line: LineString) -> bool:
        return self.indexDirective(line) != (-1, -1)

    def isBeginMacroFunc(self, line: LineString) -> bool:
        return self.indexDirective(line) == (0, -1)

    def isEndMacroFunc(self, line: LineString):
        return self.indexDirective(line) == (0, 0)

    # def processing(line: LineString) -> tuple[int, list[str]]:
    #     pass

    def isIntegrate(self, line: LineString):
        return self.indexDirective(line) == (1, -1)

    # def execute(self, obj: MacroFunction, args, foutLines: list[str]):
    #     variables = {obj.args[i]: args[i] for i in range(len(args))}

    #     for i in obj.tail:
    #         ind = self.indexDirective(i)
    #         if ind[0] != -1:
    #             name: str
    #             if ind[1] != -1:
    #                 name = self.listMacroCommand[ind[0]].endname[ind[1]]
    #             else:
    #                 name = self.listMacroCommand[ind[0]]

    #             globals()[CREATE_FUNC_COMMAND(name)]()
    #             break

    def integrate(self, line: LineString, foutLines: list[str]):
        name, args = self.getNameAndArgsMacroCommand(line)

        self.x.add_row([name + "(" + args + ")", name + str(getArgs(args))])

        # find = False
        # for i in self.macroFunctions:
        #     if i.name == name and len(i.args) == len(args):
        #         find = True
        #         self.execute(i, args, foutLines)
        #         break

        # assert find

        foutLines.append("has been integrated")


def getArgs(args: str) -> list[str]:
    returnValue: list[str] = []
    countNoClosedRoundBracket = 0
    countNoClosedQuotes = False

    for charaster in args:

        if countNoClosedRoundBracket == 0 and countNoClosedQuotes == False and charaster == ",":
            returnValue.append("")
        else:
            if len(returnValue) == 0:
                returnValue.append(charaster)
            else:
                returnValue[len(returnValue)-1] += charaster

        if charaster == "\\":
            pass

        if charaster == "\"":

            if returnValue[len(returnValue)-1][len(returnValue[len(returnValue)-1])-2] == "\\":
                returnValue[len(returnValue) - 1] = returnValue[len(returnValue) -
                                                                1][:len(returnValue[len(returnValue)-1])-2]

                returnValue[len(returnValue)-1] += "\""
            else:
                countNoClosedQuotes = not countNoClosedQuotes

        if countNoClosedQuotes == False:
            if charaster == "(":
                countNoClosedRoundBracket += 1
            elif charaster == ")":
                countNoClosedRoundBracket -= 1

    for value in returnValue:
        value = value.strip()

    assert countNoClosedRoundBracket == 0, "not closed round bracket"
    assert countNoClosedQuotes == False, "not closed quotes"

    return returnValue


def inputFileCreateTree(lines: list[LineString], macroFunc: MacroFunc, foutLines: list[str]):
    countNoClosedMacroFuncs = 0

    for line in lines:
        # import os
        # os.system("clear")
        # print(f"{i}    {line}")

        if macroFunc.isBeginMacroFunc(line):
            if countNoClosedMacroFuncs == 0:
                macroFunc.macroFunctions.append(MacroFunction([]))
            countNoClosedMacroFuncs += 1

        if countNoClosedMacroFuncs == 0 and macroFunc.isIntegrate(line):
            macroFunc.integrate(line, foutLines)

        if countNoClosedMacroFuncs > 0:
            macroFunc.macroFunctions[len(
                macroFunc.macroFunctions)-1].tail.append(line)
        else:
            foutLines.append(line.line)

        if macroFunc.isEndMacroFunc(line):
            macroFunc.macroFunctions[len(
                macroFunc.macroFunctions)-1].finalInit(macroFunc)
            countNoClosedMacroFuncs -= 1

        # print(str(macroFunc))
        # input("pause")

    assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"


# s = {"1":"hehe", "2":"sjdjs"}
# s.items


def interp(inputFile, outputFile):
    macroFunc = MacroFunc()
    macroFunc.x = PrettyTable()
    macroFunc.x.field_names = ["prev", "next"]

    with open(inputFile, "r") as fin, open(outputFile, "w") as fout:
        lines: list[LineString] = [LineString(
            i, obj.rstrip()) for i, obj in enumerate(fin.readlines())]

        foutLines = [""]

        inputFileCreateTree(lines, macroFunc, foutLines)

        fout.writelines([i+"\n" for i in foutLines])

        # print(str(macroFunc))

    print(macroFunc.x)

    for i in macroFunc.macroFunctions:
        print(i.header())
