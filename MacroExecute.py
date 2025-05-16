# модуль исполнения MacroFunc

import MacroFunc
from MacroFunc import LineString
from MacroFunction import *
from MyAlg import *
from cppGet import *
from MacroWorkWithVariables import Variables, macroSpesFunctions, is_macro, macro_value
from MacroExecuteSettings import ConditionsSaver, CicleSaver


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
            for i in variables.variables for j in i}
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


# класс исполнения макрофункции
class MacroFuncStack:
    variables: Variables
    ifelser: ConditionsSaver
    line: str
    foutLines: list[LineString]
    thisIndex: int
    cicleSaver: CicleSaver

    def printNameOfCommand(self, name):
        print("\033[37;2m", name, str(self.line), "\033[0m")

    def __init__(self):
        self.ifelser = ConditionsSaver()
        self.thisIndex = 0
        pass

    def initWithListArgs(self, func: MacroFunction, listArgs: list[str], foutLines: list[LineString], macroFunctions: ListMacroFunction):
        variables = Variables({func.args[i]: listArgs[i]
                               for i in range(len(listArgs))})
        return self.initWithVariables(func, variables, foutLines, macroFunctions)

    def initWithVariables(self, func: MacroFunction, variables: Variables, foutLines: list[LineString], macroFunctions: ListMacroFunction):
        self.variables = variables
        self.foutLines = foutLines

        startMacroFunc(func.txt, macroFunctions,
                       foutLines.copy())

        countNoClosedMacroFuncs = 0

        text: TextMacroFunction = []

        for i in range(len(func.txt)):
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
                getattr(MacroFuncStack,
                        MacroFunc.CREATE_FUNC_COMMAND(name))(self)

                i = self.thisIndex

            if ind == MacroFunc.IS_NOT_DIRECTIVE and self.ifelser.canExecute():
                foutLines.append(LineString(
                    func.txt[i].numb, processingLine(self.variables, func.txt[i].line)))

        assert countNoClosedMacroFuncs == 0, f"{countNoClosedMacroFuncs} not closed macrofunction!"

    # далее представлены функции обработки всех возможных команд MacroFunc

    @ifelser_decorator
    def macrofuncCommand(self):
        raise Exception("")

    @ifelser_decorator
    def endmacrofuncCommand(self):
        raise Exception("")

    @ifelser_decorator
    def integrateCommand(self):
        raise Exception("")

    def ifCommand(self):
        exprValue = processingLineCppGet(
            self.variables, self.line, self.foutLines)

        self.ifelser.pushIf(exprValue)

    def elifCommand(self):
        exprValue = processingLineCppGet(
            self.variables, self.line, self.foutLines)

        self.ifelser.pushElif(exprValue)

    def elseCommand(self):
        self.ifelser.pushElse()

    def endifCommand(self):
        self.ifelser.pushEndif()

    @ifelser_decorator
    def errorCommand(self):
        if self.foutLines != None:
            self.foutLines.append(
                LineString(-1, f"#if {self.line.strip()}\n   #error \"{self.line.strip()}\"\n#endif"))

    @ifelser_decorator
    def warningCommand(self):
        if self.foutLines != None:
            self.foutLines.append(
                LineString(-1, f"#if {self.line.strip()}\n   #warning \"{self.line.strip()}\"\n#endif"))

    @ifelser_decorator
    def varCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in for macrocommand"

        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLine(self.variables, args[1])

    def processingFor(self, args: list[str]) -> str:
        return args[0]

    @ifelser_decorator
    def forCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 4, "unknown args in for macrocommand"

        if self.cicleSaver.findFor(self.thisIndex):
            self.variables.deleteAreaOfVisibility()
        else:
            self.cicleSaver.declareFor(self.thisIndex)
            self.variables.newAreaOfVisibility()
            self.variables.lastAreaOfVisibility(
            )[args[0]] = processingLine(self.variables, self.processingFor(args[1:]))

        # print(args)

    @ifelser_decorator
    def endforCommand(self):
        self.cicleSaver.updateFor(self.thisIndex)
        self.variables.deleteAreaOfVisibility()
        pass

    @ifelser_decorator
    def foreachCommand(self):
        args = getStripArgs(self.line)
        assert len(args) == 2, "unknown args in foreach macrocommand"

        self.variables.newAreaOfVisibility()
        self.variables.lastAreaOfVisibility(
        )[args[0]] = processingLine(self.variables, args[1])

        # print(args)
        pass

    @ifelser_decorator
    def endforeachCommand(self):
        self.variables.deleteAreaOfVisibility()
        pass


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
