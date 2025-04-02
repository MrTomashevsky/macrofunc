import MacroFunc
from prettytable import PrettyTable
from MacroFunc import LineString
from getArgs import *
from MacroFunction import *


def CREATE_FUNC_COMMAND(name: str):
    return name + "Command"


def inputFileCreateTree(lines: list[LineString], macroFunctions: ListMacroFunction, foutLines: list[str]):
    countNoClosedMacroFuncs = 0

    text: UnprocessedTextOfMacroFunction = []

    for line in lines:
        # import os
        # os.system("clear")
        # print(f"{i}    {line}")

        if MacroFunc.isBeginMacroFunc(line):
            # if countNoClosedMacroFuncs == 0:
            #     macroFunctions.append(MacroFunction())
            countNoClosedMacroFuncs += 1

        if countNoClosedMacroFuncs == 0 and MacroFunc.isIntegrate(line):
            MacroFunc.integrate(line, foutLines)

        if countNoClosedMacroFuncs > 0:
            text.append(line)
        else:
            foutLines.append(line.line)

        if MacroFunc.isEndMacroFunc(line):

            # macroFunctions[len(
            #     macroFunctions)-1].finalInit(text, macroFunctions)
            macroFunctions.append(MacroFunction(text, macroFunctions))

            text = []
            countNoClosedMacroFuncs -= 1

        # print(str(macroFunc))
        # input("pause")

    assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"


# s = {"1":"hehe", "2":"sjdjs"}
# s.items


def interp(inputFile, outputFile):
    macroFunctions: ListMacroFunction = []
    MacroFunc.x = PrettyTable()
    MacroFunc.x.field_names = ["prev", "next"]

    with open(inputFile, "r") as fin, open(outputFile, "w") as fout:
        lines: list[LineString] = [LineString(
            i, obj.rstrip()) for i, obj in enumerate(fin.readlines())]

        foutLines = [""]

        inputFileCreateTree(lines, macroFunctions, foutLines)

        fout.writelines([i+"\n" for i in foutLines])

        # print(str(macroFunc))

    print(MacroFunc.x)

    for i in macroFunctions:
        print(str(i))
