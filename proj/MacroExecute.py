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


class Variables:
    type VarDict = dict[str, str]

    variables: list[VarDict]

    def __init__(self, variables: VarDict):
        self.variables = [variables]

    def index(self, var):
        for i in reversed(self.variables):
            ind = index(i, var)
            if ind != -1:
                return ind
        return -1

    def append(self, variables: VarDict = {}):
        self.variables.append(variables)

    def pop(self):
        self.variables.pop()

    def bask(self):
        return self.variables[len(self.variables)-1]


class MacroFuncStack:
    variables: Variables

    line: LineString
    foutLines: list[LineString]

    def printNameOfCommand(self, name):
        print("\033[37;2m", name, str(self.line), "\033[0m")

    def __init__(self, func: MacroFunction, listArgs: list[str], foutLines: list[LineString], macroFunctions: ListMacroFunction):
        self.variables = Variables({func.args[i]: listArgs[i]
                                    for i in range(len(listArgs))})
        self.foutLines = foutLines

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

                self.line = line.line[line.line.index(
                    MacroFunc.BEGIN_COMMAND) + len(MacroFunc.BEGIN_COMMAND)+len(name):]

                self.printNameOfCommand(name)
                getattr(MacroFuncStack,
                        MacroFunc.CREATE_FUNC_COMMAND(name))(self)

        assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"

    def macrofuncCommand(self):
        raise Exception("")

    def endmacrofuncCommand(self):
        raise Exception("")

    def integrateCommand(self):
        raise Exception("")

    def ifCommand(self):
        pass

    def elifCommand(self):
        pass

    def elseCommand(self):
        pass

    def endifCommand(self):
        pass

    def errorCommand(self):
        pass

        # foutLines.append(LineString(-1, "#ifdef"))

    def warningCommand(self):
        pass

    def varCommand(self):
        pass

    def forCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 4, "unknown args in for macrocommand"

        print(args)

    def endforCommand(self):
        pass

    def foreachCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in foreach macrocommand"

        print(args)
        pass

    def endforeachCommand(self):
        pass


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
