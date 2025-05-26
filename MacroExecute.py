# модуль исполнения MacroFunc

import MacroFunc
from MacroFunc import LineString
from MacroFunction import *
from MyAlg import *
from cppGet import *
from MacroWorkWithVariables import Variables, macroSpesFunctions, is_macro, macro_value
from MacroExecuteSettings import ConditionsSaver, CicleSaver, isIndex, ForInfo


def findVariable(variables: Variables, varName: str):
    for i in range(len(variables.variables)):
        if variables.variables[i].get(varName) != None:
            return i
    return -1


FOREACH_LIST = "\033"
TEMP_VAR_NAMES = [FOREACH_LIST]


def toRealType(s: str):
    for i in ["int", "float"]:
        try:
            return eval(f"{i}(string)", {}, {"string": s})
        except ValueError:
            pass
    return s


def startMacroFunc(lines: TextMacroFunction, macroFunctions: ListMacroFunction, foutLines: list[LineString]):
    countNoClosedMacroFuncs = 0

    text: TextMacroFunction = []

    for line in lines:

        if MacroFunc.isBeginMacroFunc(line):
            countNoClosedMacroFuncs += 1

        if countNoClosedMacroFuncs == 0 and MacroFunc.isIntegrate(line):
            integrate(macroFunctions, line, foutLines, True)

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
def processingLine(variables: Variables, line: str, foutLines: list[LineString]) -> str:
    # assert False, """доделай"""
    funcs = macroSpesFunctions(variables, foutLines)

    for funcName in funcs:
        indexVar = 0
        while indexVar != -1:
            indexVar = findFunction(line, indexVar, funcName)
            if indexVar != -1:
                l1 = line[:indexVar]
                # l2 = processingLineCppGet(view[funcName])

                args, sizeArgs = getArgsSpecFunction(line)

                l2 = str(funcs[funcName](args))
                l3 = line[indexVar+len(funcName)+sizeArgs:]

                while True:
                    revLine = l1[::-1].strip()
                    if index(revLine, "##") == 0:
                        l1 = l1[:len(l1)-3]
                        tmpLine = l1.split()
                        l1 = l1[:len(l1)-1 -
                                len(tmpLine[-1])] + " "
                        l2 = tmpLine[-1]+l2
                    elif index(revLine, "#") == 0:
                        l1 = l1[:len(l1)-2]
                        l2 = "\""+l2+"\""
                    else:
                        break

                line = l1+l2+l3
                indexVar += len(funcName)+sizeArgs

    for view in variables.variables:
        for var in view:
            if var != view[var]:
                indexVar = 0
                while indexVar != -1:
                    indexVar = findWord(line, indexVar, var)
                    if indexVar != -1:
                        l1 = line[:indexVar]
                        # l2 = processingLineCppGet(view[var])
                        l2 = str(view[var])
                        l3 = line[indexVar+len(var):]

                        while True:
                            revLine = l1[::-1].strip()
                            if index(revLine, "##") == 0:
                                l1 = l1[:len(l1)-3]
                                tmpLine = l1.split()
                                l1 = l1[:len(l1)-1 -
                                        len(tmpLine[-1])] + " "
                                l2 = tmpLine[-1]+l2
                            elif index(revLine, "#") == 0:
                                l1 = l1[:len(l1)-2]
                                l2 = "\""+l2+"\""
                            else:
                                break

                        line = l1+l2+l3
                        indexVar += len(var)

    tmpLine = ""
    while line != tmpLine:
        tmpLine = line
        line = delete2Charp(line)

    return line


# processingLine, но работа с cpp и вычисляемым выражением
def processingLineCppGet(variables: Variables, expr: str, foutLines: list[LineString]) -> str:
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
    funcs = macroSpesFunctions(variables, foutLines)
    vars = {j: toRealType(i[j])
            for i in variables.variables for j in i if j not in TEMP_VAR_NAMES}
    while True:
        try:
            value = eval(expr, funcs, vars)
            break
        except NameError as ne:
            if not is_macro(ne.name, foutLines):
                return False
            vars[ne.name] = toRealType(macro_value(ne.name, foutLines))

            # print(f"\033[31m{ne.name}\033[0m")

    # print(f"'{expr}' = \033[32m{value}\033[0m")

    return value


def ifelser_decorator(method, *args, **kwargs):
    def wrapper(self):
        if self.ifelser.canExecute():
            return method(self, *args, **kwargs)
    return wrapper


def forer_decorator(method, *args, **kwargs):
    def wrapper(self):
        if self.forer.canExecute():
            return method(self, *args, **kwargs)
    return wrapper


def foreacher_decorator(method, *args, **kwargs):
    def wrapper(self):
        if self.foreacher.canExecute():
            return method(self, *args, **kwargs)
    return wrapper


# класс исполнения макрофункции
class MacroFuncStack:
    variables: Variables
    line: str
    foutLines: list[LineString]
    thisIndex: int
    ifelser: ConditionsSaver
    forer: CicleSaver
    foreacher: CicleSaver
    funcName: str

    def printNameOfCommand(self, name):
        print("\033[37;2m", name, str(self.line), "\033[0m")

    def __init__(self):
        self.ifelser = ConditionsSaver()
        self.forer = CicleSaver()
        self.foreacher = CicleSaver()
        self.thisIndex = 0

    def initWithListArgs(self, func: MacroFunction, listArgs: list[str], foutLines: list[LineString], macroFunctions: ListMacroFunction):
        variables = Variables({func.args[i]: listArgs[i]
                               for i in range(len(listArgs))})
        return self.initWithVariables(func, variables, foutLines, macroFunctions)

    def initWithVariables(self, func: MacroFunction, variables: Variables, foutLines: list[LineString], macroFunctions: ListMacroFunction):
        self.funcName = func.name
        if func.name == "create_functions":
            pass
        # print("\033[35;2m", func.name, func.args, "\033[0m")

        self.variables = variables
        self.foutLines = foutLines

        startMacroFunc(func.txt, macroFunctions,
                       foutLines.copy())

        countNoClosedMacroFuncs = 0

        text: TextMacroFunction = []
        i = 0

        while i < len(func.txt):
            isSpecDirective = False
            ind = MacroFunc.indexDirective(func.txt[i])

            if MacroFunc.isIndexBeginMacroFunc(ind):
                countNoClosedMacroFuncs += 1
                isSpecDirective = True

            if countNoClosedMacroFuncs == 0 and MacroFunc.isIndexIntegrate(ind):
                integrate(macroFunctions, func.txt[i], foutLines)
                isSpecDirective = True

            if countNoClosedMacroFuncs > 0:
                text.append(func.txt[i])

            if MacroFunc.isIndexEndMacroFunc(ind):
                macroFunctions.append(MacroFunction(text))

                text = []
                countNoClosedMacroFuncs -= 1
                isSpecDirective = True

            assert ind != MacroFunc.IS_UNKNOWN_DIRECTIVE, f"unknown directive in line {func.txt[i].numb}: \"{line.line}\""

            if ind != MacroFunc.IS_NOT_DIRECTIVE and not isSpecDirective and ind[0] != -1:
                name: str
                if ind[1] != -1:
                    name = MacroFunc.listMacroCommand[ind[0]].endname[ind[1]]
                else:
                    name = MacroFunc.listMacroCommand[ind[0]].name

                self.thisIndex = i
                self.line = func.txt[i].line[func.txt[i].line.index(
                    MacroFunc.BEGIN_COMMAND) + len(MacroFunc.BEGIN_COMMAND)+len(name):]

                self.printNameOfCommand(name)
                # print(findVariable(self.variables, FOREACH_LIST) != -1)
                getattr(MacroFuncStack,
                        MacroFunc.CREATE_FUNC_COMMAND(name))(self)

                i = self.thisIndex

            if ind == MacroFunc.IS_NOT_DIRECTIVE and self.ifelser.canExecute():
                foutLines.append(LineString(
                    func.txt[i].numb, processingLine(self.variables, func.txt[i].line, self.foutLines)))

            i += 1
        assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"

    # далее представлены функции обработки всех возможных команд MacroFunc

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def macrofuncCommand(self):
        raise Exception("")

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def endmacrofuncCommand(self):
        raise Exception("")

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def integrateCommand(self):
        raise Exception("")

    @foreacher_decorator
    @forer_decorator
    def ifCommand(self):
        exprValue = processingLineCppGet(
            self.variables, self.line, self.foutLines)

        self.ifelser.pushIf(exprValue)

    @foreacher_decorator
    @forer_decorator
    def elifCommand(self):
        exprValue = processingLineCppGet(
            self.variables, self.line, self.foutLines)

        self.ifelser.pushElif(exprValue)

    @foreacher_decorator
    @forer_decorator
    def elseCommand(self):
        self.ifelser.pushElse()

    @foreacher_decorator
    @forer_decorator
    def endifCommand(self):
        self.ifelser.pushEndif()

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def errorCommand(self):
        if self.foutLines != None:
            line = processingLine(
                self.variables, self.line.strip(), self.foutLines)
            self.foutLines.append(
                LineString(-1, f"#if {line}\n   #error \"{line}\"\n#endif"))

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def warningCommand(self):
        if self.foutLines != None:
            self.foutLines.append(
                LineString(-1, f"#if {self.line.strip()}\n   #warning \"{self.line.strip()}\"\n#endif"))

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def varexprCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in for macrocommand"

        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLineCppGet(self.variables, args[1], self.foutLines)

    @foreacher_decorator
    @forer_decorator
    @ifelser_decorator
    def varlineCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in for macrocommand"

        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLine(self.variables, args[1], self.foutLines)

    @foreacher_decorator
    @ifelser_decorator
    def forCommand(self):
        if self.forer.canExecute():
            args = getStripArgs(self.line)
            assert len(args) == 4, "unknown args in for macrocommand"

            forInfoIndex = self.forer.findFor(self.thisIndex)
            forInfo: ForInfo

            if forInfoIndex == -1:
                # базовая инициализация

                self.variables.newAreaOfVisibility()
                self.variables.lastAreaOfVisibility(
                )[args[0]] = processingLine(self.variables, args[1], self.foutLines)
                forInfo = self.forer.declareFor(self.thisIndex)
            else:
                # икрементирование
                changeArg0 = processingLineCppGet(
                    self.variables, processingLine(
                        self.variables, f"{args[0]} + {args[3]}", self.foutLines), self.foutLines)

                self.variables.deleteAreaOfVisibility()
                self.variables.newAreaOfVisibility()
                self.variables.lastAreaOfVisibility()[args[0]] = changeArg0
                forInfo = self.forer.viewedCircles[forInfoIndex]

            canForExecute = processingLine(
                self.variables, f"{args[0]} != {args[2]}", self.foutLines)
            # добавить для float

            if not processingLineCppGet(self.variables, canForExecute, self.foutLines):
                self.forer.deleteLastFor()
                if isIndex(forInfo.indexEndFor):
                    self.thisIndex = forInfo.indexEndFor
                else:
                    self.forer.resetCanExecute()
        else:
            self.forer.counterFor += 1

    @foreacher_decorator
    @ifelser_decorator
    def endforCommand(self):
        if not self.forer.canExecute():
            self.forer.counterFor -= 1
        if self.forer.counterFor == 0:
            i = self.forer.findEndFor(self.thisIndex)
            if i == -1:
                self.forer.updateFor(self.thisIndex)
            self.thisIndex = self.forer.lastFor().indexFor - 1

    @forer_decorator
    @ifelser_decorator
    def foreachCommand(self):
        if self.foreacher.canExecute():
            args = getStripArgs(self.line)
            assert len(args) == 2, "unknown args in foreach macrocommand"

            forInfoIndex = self.foreacher.findFor(self.thisIndex)
            forInfo: ForInfo
            tmp: list[str]

            if forInfoIndex == -1:
                forInfo = self.foreacher.declareFor(self.thisIndex)
                tmp = processingLineCppGet(
                    self.variables, args[1], self.foutLines).split()
            else:
                forInfo = self.foreacher.viewedCircles[forInfoIndex]
                tmp = self.variables.lastAreaOfVisibility()[FOREACH_LIST]
                self.variables.deleteAreaOfVisibility()

            if len(tmp) == 0:
                self.foreacher.deleteLastFor()
                if isIndex(forInfo.indexEndFor):
                    self.thisIndex = forInfo.indexEndFor
                else:
                    self.foreacher.resetCanExecute()
            else:
                self.variables.newAreaOfVisibility()
                self.variables.lastAreaOfVisibility()[FOREACH_LIST] = tmp[1:]
                self.variables.lastAreaOfVisibility()[args[0]] = tmp[0]
        else:
            self.foreacher.counterFor += 1

    @forer_decorator
    @ifelser_decorator
    def endforeachCommand(self):
        if not self.foreacher.canExecute():
            self.foreacher.counterFor -= 1
        if self.foreacher.counterFor == 0:
            i = self.foreacher.findEndFor(self.thisIndex)
            if i == -1:
                self.foreacher.updateFor(self.thisIndex)
            self.thisIndex = self.foreacher.lastFor().indexFor - 1


def getVariablesWithCppGet(func: MacroFunction, listArgs: list[str], foutLines: list[LineString]):
    def cppGetVariable(varValue):
        if is_macro(varValue, foutLines):
            return macro_value(varValue, foutLines)
        return varValue

    variables = Variables({func.args[i]: cppGetVariable(listArgs[i])
                           for i in range(len(listArgs))})
    return variables


# исполнение макрофункции
def integrate(macroFunctions: ListMacroFunction, line: LineString, foutLines: list[LineString], getMacroWithCppGet=False):

    name, args = MacroFunc.getNameAndArgsMacroCommand(line)

    listArgs = getArgs(args)

    # print(f"\033[34m{name, listArgs}\033[0m")
    find = False

    reversedMacroFunctions = reversed(macroFunctions)

    for func in reversedMacroFunctions:
        f1 = func.name == name
        f2 = len(listArgs) == len(func.args)
        if f1 and f2:
            find = True

            execute = MacroFuncStack()

            if getMacroWithCppGet:
                if name == "create_functions":
                    pass
                variables = getVariablesWithCppGet(
                    func, listArgs, foutLines)
                execute.initWithVariables(
                    func, variables, foutLines, macroFunctions.copy())
            else:
                execute.initWithListArgs(
                    func, listArgs, foutLines, macroFunctions.copy())
            break

    arr = ""
    for i in macroFunctions:
        arr += i.determination() + "\n"

    assert find, f"{name}{listArgs} in\n {arr} not find!"

    # foutLines.append("has been integrated")
