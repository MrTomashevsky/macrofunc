from MyAlg import *
from cppLanguageInfo import is_cstr
from MacroFunc import LineString
import cppGet
import TmpFile


class MacroVariablesException(Exception):
    pass


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


def macro_value(var: MacroVariable, foutLines: list[LineString]) -> str:
    return cppGet.value([i.line+"\n" for i in foutLines if i.line !=
                         "" and not i.line.isspace()], var)


def is_macro(var: MacroVariable, foutLines: list[LineString]) -> bool:
    return cppGet.isDef([i.line+"\n" for i in foutLines if i.line !=
                         "" and not i.line.isspace()], var)


def create__IS_VOID__(variables: Variables):
    return lambda var: not is_var(var, variables) or variables.variables[var] == ""


def create__IS_INT__(variables: Variables):
    def f(var):
        # if is_var(var, variables):
        try:
            i = int(variables.variables[var])
            return True
        except ValueError:
            pass
        return False
    return f


def create__IS_FLOAT__(variables: Variables):
    def f(var):
        # if is_var(var, variables):
        try:
            i = float(variables.variables[var])
            return True
        except ValueError:
            pass
        return False
    return f


def create__IS_CSTR__(variables: Variables):
    return lambda var:  is_cstr(variables.variables[str(var)])


def create__IS_MACRO__(foutLines: list[LineString]):
    return lambda var: is_macro(str(var), foutLines)


def create__IS_WORD__():
    return lambda var: len(str(var).split()) == 1


def create__IS_LIST__():
    return lambda var: len(str(var).split()) > 1


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


# def error_if_is_not_list(var):
#     if create__IS_LIST__()(var):
#         return True
#     raise MacroVariablesException(f"is not list: '{var}'")


def create__SIZE_LIST__():
    def f(lst):
        # error_if_is_not_list(lst)
        return len(str(lst).split())
    return f


def create__IS_END_LIST__(variables: Variables):
    # error_if_is_not_list(var, variables) and
    return lambda lst, var:  var == lst.split()[-1]


def create__IS_BEGIN_LIST__(variables: Variables):
    # error_if_is_not_list(var, variables) and
    return lambda lst, var:   var == lst.split()[0]


def create__IS_ITEM_LIST__(variables: Variables):
    # error_if_is_not_list(var, variables) and
    return lambda lst, var:   var in lst.split()


def create__INDEX__(variables: Variables):
    def f(lst, var):
        error_if_is_not_list(var, variables)
        ind = index(lst.split(), var)
        if ind == -1:
            return ""
        return f"{ind}"
    return f


"""
Над списком также можно использовать некоторые спецфункции:
- __SIZE_LIST__ - возвращает количество слов в списке
-  __IS_END_LIST__ - истина, если аргумент - последний элемент в списке(если список пустой - всегда ложь)
- __IS_BEGIN_LIST__ - тоже самое, но для начального элемента
- __IS_ITEM_LIST__ - истина, если аргумент есть в списке
- __INDEX__ - возвращает элемент списка по индексу(возвращает пустоту, если индекс расположен за границами списка).
"""


def macroSpesFunctions(variables: Variables, foutLines: list[LineString]) -> dict[str, ]:
    returnValue: dict[str, ] = {}

    returnValue["__IS_VOID__"] = create__IS_VOID__(variables)
    returnValue["__IS_INT__"] = create__IS_INT__(variables)
    returnValue["__IS_FLOAT__"] = create__IS_FLOAT__(variables)
    returnValue["__IS_CSTR__"] = create__IS_CSTR__(variables)
    returnValue["__IS_MACRO__"] = create__IS_MACRO__(foutLines)
    returnValue["__IS_WORD__"] = create__IS_WORD__()
    returnValue["__IS_LIST__"] = create__IS_LIST__()

    returnValue["__SIZE_LIST__"] = create__SIZE_LIST__()
    returnValue["__IS_END_LIST__"] = create__IS_END_LIST__(variables)
    returnValue["__IS_BEGIN_LIST__"] = create__IS_BEGIN_LIST__(variables)
    returnValue["__IS_ITEM_LIST__"] = create__IS_ITEM_LIST__(variables)
    returnValue["__INDEX__"] = create__INDEX__(variables)

    return returnValue
