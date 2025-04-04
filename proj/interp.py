import MacroFunc
from MacroFunc import LineString
import MacroFunction
import MacroExecute

# from prettytable import PrettyTable


def interp(inputFile, outputFile):
    macroFunctions: MacroFunction.ListMacroFunction = []
    # MacroFunc.x = PrettyTable()
    # MacroFunc.x.field_names = ["prev", "next"]

    with open(inputFile, "r") as fin, open(outputFile, "w") as fout:
        lines: MacroFunc.TextMacroFunction = [LineString(
            i, obj.rstrip()) for i, obj in enumerate(fin.readlines())]

        foutLines: list[LineString] = []

        MacroExecute.startMacroFunc(lines, macroFunctions, foutLines)

        fout.writelines([i.line for i in foutLines])

        # print(str(macroFunc))

    # print(MacroFunc.x)

    for i in macroFunctions:
        print(str(i))
