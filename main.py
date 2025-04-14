from clah import Command, Type, Argument, commandLineAgrumentHandler
import sys

import MacroFunc
from MacroFunc import LineString
import MacroFunction
import MacroExecute
# from prettytable import PrettyTable


argv = ["create",
        "source/cpp.cpp",
        "source/cpp2.cpp"
        ]  # sys.argv[1:]


def create(args: list):
    macroFunctions: MacroFunction.ListMacroFunction = []
    # MacroFunc.x = PrettyTable()
    # MacroFunc.x.field_names = ["prev", "next"]
    foutLines: list[LineString] = []

    with open(args[0], "r") as fin:
        lines: MacroFunc.TextMacroFunction = [LineString(0, "")]+[LineString(
            i, obj.rstrip()) for i, obj in enumerate(fin.readlines())]

        MacroExecute.startMacroFunc(lines, macroFunctions, foutLines)

    with open(args[1], "w") as fout:
        fout.writelines([i.line+"\n" for i in foutLines])


def help(args: list):
    pass


commands = [
    Command("--help", [], help),
    Command("create", [Argument(Type.FILE), Argument(Type.FILE)], create)
]

commandLineAgrumentHandler(argv, commands)
