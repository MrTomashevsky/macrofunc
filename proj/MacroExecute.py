import MacroFunc
from MacroFunc import LineString
from MacroFunction import *
from MyAlg import *
# from MyAlg import *


def startMacroFunc(lines: TextMacroFunction, macroFunctions: ListMacroFunction, foutLines: list[LineString]):
    countNoClosedMacroFuncs = 0

    text: TextMacroFunction = []

    for line in lines:
        # import os
        # os.system("clear")
        # print(f"{i}    {line}")

        if MacroFunc.isBeginMacroFunc(line):
            # if countNoClosedMacroFuncs == 0:
            #     macroFunctions.append(MacroFunction())
            countNoClosedMacroFuncs += 1

        if countNoClosedMacroFuncs == 0 and MacroFunc.isIntegrate(line):
            integrate(line, foutLines)

        if countNoClosedMacroFuncs > 0:
            text.append(line)
        else:
            if foutLines != None:
                foutLines.append(line)

        if MacroFunc.isEndMacroFunc(line):

            # macroFunctions[len(
            #     macroFunctions)-1].finalInit(text, macroFunctions)
            macroFunctions.append(MacroFunction(text, macroFunctions))

            text = []
            countNoClosedMacroFuncs -= 1

        # print(str(macroFunc))
        # input("pause")

    assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"


class MacroFuncStack:
    variables: dict[str, str]

    def __init__(self, func: MacroFunction, listArgs: list[str], foutLines: list[LineString], macroFunctions: ListMacroFunction):
        self.variables = {func.args[i]: listArgs[i]
                          for i in range(len(listArgs))}

        startMacroFunc(func.txt, macroFunctions, None)

        for line in func.txt:
            ind = MacroFunc.indexDirective(line)
            if ind[0] != -1:
                name: str
                if ind[1] != -1:
                    name = MacroFunc.listMacroCommand[ind[0]].endname[ind[1]]
                else:
                    name = MacroFunc.listMacroCommand[ind[0]]

                getattr(MacroFuncStack,
                        MacroFunc.CREATE_FUNC_COMMAND(name))(self, line)
                break

    # def macrofuncCommand(self, line: LineString):
    #     assert False

    # def endmacrofuncCommand(self, line: LineString):
    #     pass

    # def integrateCommand(self, line: LineString):
    #     pass

    def ifCommand(self, line: LineString):
        pass

    def elifCommand(self, line: LineString):
        pass

    def elseCommand(self, line: LineString):
        pass

    def endifCommand(self, line: LineString):
        pass

    def errorCommand(self, line: LineString):
        pass

    def warningCommand(self, line: LineString):
        pass

    def varCommand(self, line: LineString):
        pass

    def forCommand(self, line: LineString):
        pass

    def endforCommand(self, line: LineString):
        pass

    def foreachCommand(self, line: LineString):
        pass

    def endforeachCommand(self, line: LineString):
        pass


def integrate(macroFunctions: ListMacroFunction, line: LineString, foutLines: list[LineString]):

    name, args = MacroFunc.getNameAndArgsMacroCommand(line)
    listArgs = getArgs(args)

    # global x
    # x.add_row([name + "(" + args + ")", name + str(listArgs)])

    find = False
    for func in macroFunctions:
        if func.name == name and len(listArgs) == len(args):
            find = True
            MacroFuncStack(func, listArgs, foutLines, macroFunctions.copy())
            break

    assert find

    foutLines.append("has been integrated")
