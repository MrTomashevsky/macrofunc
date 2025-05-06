# модуль обработки макрофункций

import MacroFunc
import cppLanguageInfo
from MacroFunc import LineString, TextMacroFunction
from MyAlg import *

type ListMacroFunction = list[MacroFunction]


# класс макрофункции; хранит имя, список аргумент и тело
class MacroFunction:
    name: str = ""
    args: list[str] = []
    txt: TextMacroFunction = []

    # получить имя + аргументы в формате строки
    def determination(self):
        return f"{self.name}{self.args}"

    # получить макрофункцию в формате строки
    def __str__(self):
        returnValue = self.name + str(self.args) + "\n"
        for j in self.txt:
            returnValue = returnValue + str(j) + "\n"
        return returnValue

    def __init__(self, text: TextMacroFunction):
        # получение имени и аргументов
        def createHeader(text):
            line = text[0]
            self.name, args = MacroFunc.getNameAndArgsMacroCommand(line)
            self.args = getArgs(args)

        # выполнение strip над строрками без директив
        def initMacroFunction(text: TextMacroFunction):
            assert MacroFunc.isBeginMacroFunc(text[0])
            assert MacroFunc.isEndMacroFunc(text[len(text)-1])

            text = text[1:len(text)-1]
            text = [i for i in text if not i.line.strip() == ""]

            for i in text:
                if MacroFunc.indexDirective(i) == MacroFunc.IS_NOT_DIRECTIVE:
                    i.line = i.line.strip()

            return text

        createHeader(text)
        self.txt = initMacroFunction(text)
