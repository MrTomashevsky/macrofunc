from clah import Command, Type, Argument, commandLineAgrumentHandler
import sys

import MacroFunc
from MacroFunc import LineString
import MacroFunction
import MacroExecute

# from prettytable import PrettyTable


argv = ["create",
        "/home/tomatik/project/kurs_proj/source/cpp.cpp",
        "/home/tomatik/project/kurs_proj/source/cpp2.cpp"
        ]  # sys.argv[1:]


# argv = ["create",
#         "/home/tomatik/project/kurs_proj/source/cppMacro.cpp",
#         "/home/tomatik/project/kurs_proj/source/cppMacro2.cpp"
#         ]  # sys.argv[1:]


def create(args: list):
    macroFunctions: MacroFunction.ListMacroFunction = []
    # MacroFunc.x = PrettyTable()
    # MacroFunc.x.field_names = ["prev", "next"]

    with open(args[0], "r") as fin, open(args[1], "w") as fout:
        lines: MacroFunc.TextMacroFunction = [LineString(0, "")]+[LineString(
            i, obj.rstrip()) for i, obj in enumerate(fin.readlines())]

        foutLines: list[LineString] = []

        MacroExecute.startMacroFunc(lines, macroFunctions, foutLines)

        fout.writelines([i.line+"\n" for i in foutLines])

        # print(str(macroFunc))

    # print(MacroFunc.x)

    # for i in macroFunctions:
    #     print(str(i))


def help(args: list):
    print('help', args)


commands = [
    Command("--help", [], help),
    Command("create", [Argument(Type.FILE), Argument(Type.FILE)], create)
]

# /bin/python /home/tomatik/project/kurs_proj/proj/main.py create /home/tomatik/project/kurs_proj/source/cpp.cpp /home/tomatik/project/kurs_proj/source/cpp2.cpp


# try:
commandLineAgrumentHandler(argv, commands)
# except Exception as ex:
#     print(ex)
