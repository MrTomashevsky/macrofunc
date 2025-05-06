# модуль исполнения MacroFunc

import MacroFunc
from MacroFunc import LineString
from MacroFunction import *
from MyAlg import *
from cppGet import *
from MacroWorkWithVariables import Variables
from MacroWorkWithVariables import macroSpesFunctions


def startMacroFunc(lines: TextMacroFunction, macroFunctions: ListMacroFunction, foutLines: list[LineString], inputFileName: str):
    countNoClosedMacroFuncs = 0

    text: TextMacroFunction = []

    for line in lines:

        if line.numb == 134:
            pass

        if MacroFunc.isBeginMacroFunc(line):
            countNoClosedMacroFuncs += 1

        if countNoClosedMacroFuncs == 0 and MacroFunc.isIntegrate(line):
            integrate(macroFunctions, line, foutLines, inputFileName)

        if countNoClosedMacroFuncs > 0:
            text.append(line)
        elif not MacroFunc.isDirective(line) and foutLines != None:
            foutLines.append(line)

        if MacroFunc.isEndMacroFunc(line):
            if countNoClosedMacroFuncs == 1:
                macroFunctions.append(MacroFunction(text))

                text = []
            countNoClosedMacroFuncs -= 1

    assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"


# функция обработки бездиррективной строки (вставка значений переменных, объединение лексем и тд)
def processingLine(variables: Variables, line: str) -> str:
    def isalnum(l: str, index: int):
        return index < 0 and index >= len(l) or (index >= 0 and index < len(l) and l[index].isalnum())

    for view in variables.variables:
        for var in view:
            if var != view[var]:
                indexVar = 0
                while indexVar != -1:
                    indexVar = line.find(var)
                    if indexVar != -1 and not isalnum(line, indexVar-1) and not isalnum(line, indexVar+len(var)+1):

                        l1 = line[:indexVar]
                        # l2 = processingLineCppGet(view[var])
                        l2 = view[var]
                        l3 = line[indexVar+len(var):]

                        while True:
                            revLine = l1[::-1].strip()
                            if index(revLine, "##") == 0:
                                l1 = l1[:len(l1)-3]
                                tmpLine = l1.split()
                                l1 = l1[:len(l1)-1 -
                                        len(tmpLine[len(tmpLine)-1])]
                                l2 = tmpLine[len(tmpLine)-1]+l2
                            elif index(revLine, "#") == 0:
                                l1 = l1[:len(l1)-2]
                                l2 = "\""+l2+"\""
                            else:
                                break

                        line = l1+l2+l3

    # indexResh = index(line, "##")
    # while indexResh != -1:
    #     indexResh = index(line, "##")
    #     line = line[:indexResh].rstrip(
    #     ) + line[indexResh+len("##"):].lstrip()

    return line


# processingLine, но работа с cpp и вычисляемым выражением
def processingLineCppGet(variables: Variables, expr: str, inputFileName: str, foutLines: list[LineString]) -> str:
    # expr = processingLine(variables, expr)

    replacement: dict[str, str] = {
        "!": " not ",
        "not =": "!=",  # эта строка сбрасывает '!='->'not ='
        "||": " or ",
        "&&": " and "
    }

    for i in replacement:
        while True:
            indexWord = index(expr, i)
            if indexWord == -1:
                break
            tmpExpr = expr[:indexWord]
            expr = tmpExpr + replacement[i] + expr[len(tmpExpr)+len(i):]

    value = None
    try:
        funcs = macroSpesFunctions(
            variables, inputFileName, foutLines)
        vars = {j: i[j] for i in variables.variables for j in i}
        value = eval(expr, funcs, vars)
    except NameError as ne:
        value = f"\033[31mError:{ne}\033[0m"

    print(f"'{expr}' = {value}")

    # raise Exception("not work func")
    return expr


# класс исполнения макрофункции
class MacroFuncStack:
    variables: Variables

    line: str
    foutLines: list[LineString]
    inputFileName: str

    def printNameOfCommand(self, name):
        print("\033[37;2m", name, str(self.line), "\033[0m")

    def __init__(self, func: MacroFunction, listArgs: list[str], foutLines: list[LineString], macroFunctions: ListMacroFunction, inputFileName: str):
        self.variables = Variables({func.args[i]: listArgs[i]
                                    for i in range(len(listArgs))})
        self.foutLines = foutLines
        self.inputFileName = inputFileName

        startMacroFunc(func.txt, macroFunctions, None, inputFileName)

        countNoClosedMacroFuncs = 0

        text: TextMacroFunction = []

        for line in func.txt:
            isSpecDirective = False
            ind = MacroFunc.indexDirective(line)

            if MacroFunc.isIndexBeginMacroFunc(ind):
                countNoClosedMacroFuncs += 1
                isSpecDirective = True

            if countNoClosedMacroFuncs == 0 and MacroFunc.isIndexIntegrate(ind):
                integrate(macroFunctions, line, foutLines, inputFileName)
                isSpecDirective = True

            if countNoClosedMacroFuncs > 0:
                text.append(line)

            if MacroFunc.isIndexEndMacroFunc(ind):
                macroFunctions.append(MacroFunction(text))

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

            if ind == MacroFunc.IS_NOT_DIRECTIVE:

                foutLines.append(LineString(
                    line.numb, processingLine(self.variables, line.line)))

        assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"

    # далее представлены функции обработки всех возможных команд MacroFunc

    def macrofuncCommand(self):
        raise Exception("")

    def endmacrofuncCommand(self):
        raise Exception("")

    def integrateCommand(self):
        raise Exception("")

    def ifCommand(self):
        exprValue = processingLineCppGet(
            self.variables, self.line, self.inputFileName, self.foutLines)
        pass

    def elifCommand(self):
        exprValue = processingLineCppGet(
            self.variables, self.line, self.inputFileName, self.foutLines)
        pass

    def elseCommand(self):
        pass

    def endifCommand(self):
        pass

    def errorCommand(self):
        if self.foutLines != None:
            self.foutLines.append(
                LineString(-1, f"#if {self.line.strip()}\n   #error \"{self.line.strip()}\"\n#endif"))

    def warningCommand(self):
        if self.foutLines != None:
            self.foutLines.append(
                LineString(-1, f"#if {self.line.strip()}\n   #warning \"{self.line.strip()}\"\n#endif"))

    def varCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in for macrocommand"

        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLine(self.variables, args[1])

    def forCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 4, "unknown args in for macrocommand"

        self.variables.newAreaOfVisibility()
        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLine(self.variables, args[1])

        print(args)

    def endforCommand(self):
        self.variables.deleteAreaOfVisibility()
        pass

    def foreachCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in foreach macrocommand"

        self.variables.newAreaOfVisibility()
        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLine(self.variables, args[1])

        print(args)
        pass

    def endforeachCommand(self):
        self.variables.deleteAreaOfVisibility()
        pass


# исполнение макрофункции
def integrate(macroFunctions: ListMacroFunction, line: LineString, foutLines: list[LineString], inputFileName: str):

    name, args = MacroFunc.getNameAndArgsMacroCommand(line)
    listArgs = getArgs(args)

    # global x
    # x.add_row([name + "(" + args + ")", name + str(listArgs)])
    print(f"\033[34m{name, listArgs}\033[0m")
    find = False

    reversedMacroFunctions = reversed(macroFunctions)

    for func in reversedMacroFunctions:
        f1 = func.name == name
        f2 = len(listArgs) == len(func.args)
        if f1 and f2:
            find = True

            MacroFuncStack(func, listArgs, foutLines,
                           macroFunctions.copy(), inputFileName)
            break

    arr = ""
    for i in macroFunctions:
        arr += i.determination() + "\n"

    assert find, f"{name}{listArgs} in\n {arr} not find!"

    # foutLines.append("has been integrated")
