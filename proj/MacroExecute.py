import MacroFunc
from MacroFunc import LineString
from MacroFunction import *
from MyAlg import *
# from MyAlg import *


def startMacroFunc(lines: TextMacroFunction, macroFunctions: ListMacroFunction, foutLines: list[LineString]):
    countNoClosedMacroFuncs = 0

    text: TextMacroFunction = []

    for line in lines:

        if line.numb == 134:
            pass

        if MacroFunc.isBeginMacroFunc(line):
            countNoClosedMacroFuncs += 1

        if countNoClosedMacroFuncs == 0 and MacroFunc.isIntegrate(line):
            integrate(macroFunctions, line, foutLines)

        if countNoClosedMacroFuncs > 0:
            text.append(line)
        else:
            if foutLines != None:
                foutLines.append(line)

        if MacroFunc.isEndMacroFunc(line):
            if countNoClosedMacroFuncs == 1:
                macroFunctions.append(MacroFunction(text, macroFunctions))

                text = []
            countNoClosedMacroFuncs -= 1

    assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"


class MacroFuncStack:
    variables: dict[str, str]

    def __init__(self, func: MacroFunction, listArgs: list[str], foutLines: list[LineString], macroFunctions: ListMacroFunction):
        self.variables = {func.args[i]: listArgs[i]
                          for i in range(len(listArgs))}

        startMacroFunc(func.txt, macroFunctions, None)

        countNoClosedMacroFuncs = 0

        text: TextMacroFunction = []

        for line in func.txt:
            isSpecDirective = False
            ind = MacroFunc.indexDirective(line)

            if MacroFunc.isIndexBeginMacroFunc(ind):
                countNoClosedMacroFuncs += 1
                isSpecDirective = True

            if countNoClosedMacroFuncs == 0 and MacroFunc.isIndexIntegrate(ind):
                integrate(macroFunctions, line, foutLines)
                isSpecDirective = True

            if countNoClosedMacroFuncs > 0:
                text.append(line)
            else:
                if foutLines != None:
                    foutLines.append(line)

            if MacroFunc.isIndexEndMacroFunc(ind):
                macroFunctions.append(MacroFunction(text, macroFunctions))

                text = []
                countNoClosedMacroFuncs -= 1
                isSpecDirective = True

            assert ind != MacroFunc.IS_UNKNOWN_DIRECTIVE, f"unknown directive in line {line.numb}: \"{line.line}\""

            if ind != MacroFunc.IS_NOT_DIRECTIVE and not isSpecDirective and ind[0] != -1:
                name: str
                if ind[1] != -1:
                    name = MacroFunc.listMacroCommand[ind[0]].endname[ind[1]]
                else:
                    name = MacroFunc.listMacroCommand[ind[0]].name

                getattr(MacroFuncStack,
                        MacroFunc.CREATE_FUNC_COMMAND(name))(self, line)

        assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"

    def macrofuncCommand(self, line: LineString):
        print("\033[37;2mmacrofuncCommand", str(line), "\033[0m")

    def endmacrofuncCommand(self, line: LineString):
        print("\033[37;2mendmacrofuncCommand", str(line), "\033[0m")

    def integrateCommand(self, line: LineString):
        print("\033[37;2mintegrateCommand", str(line), "\033[0m")

    def ifCommand(self, line: LineString):
        print("\033[37;2mifCommand", str(line), "\033[0m")

    def elifCommand(self, line: LineString):
        print("\033[37;2melifCommand", str(line), "\033[0m")

    def elseCommand(self, line: LineString):
        print("\033[37;2melseCommand", str(line), "\033[0m")

    def endifCommand(self, line: LineString):
        print("\033[37;2mendifCommand", str(line), "\033[0m")

    def errorCommand(self, line: LineString):
        print("\033[37;2merrorCommand", str(line), "\033[0m")

    def warningCommand(self, line: LineString):
        print("\033[37;2mwarningCommand", str(line), "\033[0m")

    def varCommand(self, line: LineString):
        print("\033[37;2mvarCommand", str(line), "\033[0m")

    def forCommand(self, line: LineString):
        print("\033[37;2mforCommand", str(line), "\033[0m")

    def endforCommand(self, line: LineString):
        print("\033[37;2mendforCommand", str(line), "\033[0m")

    def foreachCommand(self, line: LineString):
        print("\033[37;2mforeachCommand", str(line), "\033[0m")

    def endforeachCommand(self, line: LineString):
        print("\033[37;2mendforeachCommand", str(line), "\033[0m")


def integrate(macroFunctions: ListMacroFunction, line: LineString, foutLines: list[LineString]):

    name, args = MacroFunc.getNameAndArgsMacroCommand(line)
    listArgs = getArgs(args)

    # global x
    # x.add_row([name + "(" + args + ")", name + str(listArgs)])
    print(f"\033[34m{name, listArgs}\033[0m")
    find = False
    for func in macroFunctions:
        f1 = func.name == name
        f2 = len(listArgs) == len(func.args)
        if f1 and f2:
            find = True

            MacroFuncStack(func, listArgs, foutLines, macroFunctions.copy())
            break

    arr = ""
    for i in macroFunctions:
        arr += i.determination() + "\n"

    assert find, f"{name}{listArgs} in\n {arr} not find!"

    # foutLines.append("has been integrated")
