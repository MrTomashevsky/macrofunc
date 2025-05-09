from clah2 import *
import sys

import MacroFunc
from MacroFunc import LineString
import MacroFunction
import MacroExecute
import cppLanguageInfo
import GlobalOneTmpFile

stdout = None


def process(args: list):
    macroFunctions: MacroFunction.ListMacroFunction = []
    foutLines: list[LineString] = []

    with open(args[0], "r") as fin:
        lines: MacroFunc.TextMacroFunction = [LineString(0, "")]+[LineString(
            i, obj.rstrip()) for i, obj in enumerate(fin.readlines())]

        # удаление с++ комменатриев из макрофункции
        def deleteComments(text):
            tmptext = []
            isMultiLineComment = False
            ind: int
            for i in text:
                line = i.line

                if isMultiLineComment:
                    ind = cppLanguageInfo.indexEndMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = False
                        line = line[ind+len(MacroFunc.BEGIN_COMMAND):]
                    else:
                        line = ""
                else:
                    ind = cppLanguageInfo.indexBeginMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = True
                        line = line[:ind]

                ind = cppLanguageInfo.indexSingleLineComment(i.line)
                if ind != -1:
                    line = line[:ind]

                tmptext.append(LineString(i.numb, line))

            return tmptext

        lines = deleteComments(lines)

        # for line in lines:
        #     print(line.numb, " ", line.line)
        # exit()
        MacroExecute.startMacroFunc(lines, macroFunctions, foutLines, args[0])

    outputLines = [i.line+"\n" for i in foutLines if not i.line.isspace()
                   and i.line != ""]

    if stdout == None:
        sys.stdout.writelines(outputLines)
    else:
        with open(stdout, "w") as fout:
            fout.writelines(outputLines)

    GlobalOneTmpFile.clear()


def help(args: list):
    nameProg = "MacroFunc"  # sys.argv[0]
    blueBegin = "\033[34;1m"
    greenBegin = "\033[32;1;2m"
    macroFuncBegin = greenBegin
    end = "\033[0m"
    print(
        f"""{blueBegin}Использование:{end}
  {macroFuncBegin}{nameProg}{end}[ключи] файл.

{blueBegin}Описание:{end}
  {macroFuncBegin}{nameProg}{end} - это программа интерпретатора {macroFuncBegin}MacroFunc{end}. На вход подаётся обрабатываемый файл.

{blueBegin}Ключи:{end}
  -h, --help                             Вывести справку.
  --def_cstr_literals <файл>             Расположение файла литералов с-строк.
  -o <файл>                              Направить вывод в файл.

{blueBegin}Автор:{end}
  Никита Томашевский, 2025, https://github.com/MrTomashevsky/macrofunc""")
    exit(0)


def o(args: list):
    global stdout
    stdout = args[0]


def def_cstr_literals(args: list):
    with open(args[0], "r") as fin:
        cppLanguageInfo.permissibleStringLiterals = [
            i.strip().replace("\n", "") for i in fin.readlines() if not i.isspace() and i != ""]


main = Command(
    None,
    [Key("help", "h", [], help),
     Key("def_cstr_literals", None, [PrimitiveType.FILE], def_cstr_literals),
     Key(None, "o", [Type.STRING], o)],
    [Type.FILE],
    [],
    process
)

# main.commands.append(main)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as ex:
        print(f"\033[31m{ex}\033[0m")
