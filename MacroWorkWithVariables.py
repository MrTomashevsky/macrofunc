from MyAlg import *
from cppLanguageInfo import is_cstr
from MacroFunc import LineString
import cppGet
import os

# класс, занимающийся хранением и осуществлением доступа к переменным в разных областях видимости


class Variables:
    type VarDict = dict[str, str]

    variables: list[VarDict]

    def __init__(self, variables: VarDict):
        self.variables = [variables]

    # найти переменную
    def index(self, var):
        for i in reversed(self.variables):
            ind = index(i, var)
            if ind != -1:
                return ind
        return -1

    # добавить новую область видимости
    def newAreaOfVisibility(self, variables: VarDict = {}):
        self.variables.append(variables)

    # выйти из области видимости
    def deleteAreaOfVisibility(self):
        self.variables.pop()

    # доступ к последней области видимости
    def lastAreaOfVisibility(self):
        return self.variables[len(self.variables)-1]


type MacroVariable = str

# здесь будут специальные функции, используемые при парсинге


def is_var(var: MacroVariable, variables: Variables) -> bool:
    return var in variables.variables


def is_macro(var: MacroVariable, inputFileName: str, foutLines: list[LineString]) -> bool:
    TMP_FILE_NAME = ".tmp.cpp"

    outputLines = [i.line+"\n" for i in foutLines if i.line !=
                   "" and not i.line.isspace()]
    with open(TMP_FILE_NAME, "w") as tmpFile:
        tmpFile.writelines(outputLines)
    if not cppGet.isDef(TMP_FILE_NAME, var):
        for i in foutLines:
            print(i.numb, " ", i.line)
        exit()
    os.remove(TMP_FILE_NAME)

    return True


def __IS_VOID__(variables: Variables, inputFileName: str):
    return lambda var: not is_var(var, variables) or variables.variables[var] == ""


def __IS_INT__(variables: Variables, inputFileName: str):
    def f(var):
        if is_var(var, variables):
            try:
                i = int(variables.variables[var])
                return True
            except ValueError:
                pass
        return False
    return f


def __IS_FLOAT__(variables: Variables, inputFileName: str):
    def f(var):
        if is_var(var, variables):
            try:
                i = float(variables.variables[var])
                return True
            except ValueError:
                pass
        return False
    return f


def __IS_CSTR__(variables: Variables, inputFileName: str):
    return lambda var: is_var(var, variables) and is_cstr(variables.variables[var])


def __IS_MACRO__(variables: Variables, inputFileName: str, foutLines: list[LineString]):
    return lambda var: is_var(var, variables) or is_macro(var, inputFileName, foutLines)


"""
Для того, чтобы определить, какой тип данных у переменной, в условиях ##if, ##elif можно использовать спецфункции:
- "__IS_VOID__" - возвращает истину, если переменная пустой;
- "__IS_INT__" - возвращает истину, если переменная - целое число;
- "__IS_FLOAT__" - возвращает истину, если переменная - дробное число;
- "__IS_CSTR__" - вовзращает истину, если переменная - С-строка;
- "__IS_MACRO__" - возвращает истину, если переменная содержит другую переменную;
- "__IS_WORD__" - возвращает истину, если переменная - одно слово;
- "__IS_LIST__" - возвращает истину, если переменная - список.
Каждая спецфункция принимает один аргумент - имя переменной.
"""

"""
Над списком также можно использовать некоторые спецфункции:
- __SIZE_LIST__ - возвращает количество слов в списке
-  __IS_END_LIST__ - истина, если аргумент - последний элемент в списке(если список пустой - всегда ложь)
- __IS_BEGIN_LIST__ - тоже самое, но для начального элемента
- __IS_ITEM_LIST__ - истина, если аргумент есть в списке
- __INDEX__ - возвращает элемент списка по индексу(возвращает пустоту, если индекс расположен за границами списка).
"""


def macroSpesFunctions(variables: Variables, inputFileName: str, foutLines: list[LineString]) -> dict[str, ]:
    returnValue: dict[str, ] = {}

    # returnValue["__IS_VOID__"] = __IS_VOID__(variables, inputFileName)
    returnValue["__IS_MACRO__"] = __IS_MACRO__(
        variables, inputFileName, foutLines)

    return returnValue
