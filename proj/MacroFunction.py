# модуль обработки макрофункций

import MacroFunc
import cppComments
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

    def __init__(self, text: TextMacroFunction, macroFunctions: ListMacroFunction):
        # получение имени и аргументов
        def createHeader(text):
            line = text[0]
            self.name, args = MacroFunc.getNameAndArgsMacroCommand(line)
            self.args = getArgs(args)

        # удаление с++ комменатриев из макрофункции
        def deleteComments(text):
            tmptext = []
            isMultiLineComment = False
            ind: int
            for i in text:
                line = i.line

                if isMultiLineComment:
                    ind = cppComments.indexEndMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = False
                        line = line[ind+len(MacroFunc.BEGIN_COMMAND):]
                    else:
                        line = ""
                else:
                    ind = cppComments.indexBeginMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = True
                        line = line[:ind]

                ind = cppComments.indexSingleLineComment(i.line)
                if ind != -1:
                    line = line[:ind]

                tmptext.append(LineString(i.numb, line))

            return tmptext

        # удаление macrofunc и endmacrofunc из текста +
        # выполнение strip над строрками без директив
        def initMacroFunction(text: TextMacroFunction, macroFunctions: ListMacroFunction):
            assert MacroFunc.isBeginMacroFunc(text[0])
            assert MacroFunc.isEndMacroFunc(text[len(text)-1])

            text = text[1:len(text)-1]
            text = [i for i in text if not i.line.strip() == ""]

            for i in text:
                if MacroFunc.indexDirective(i) == MacroFunc.IS_NOT_DIRECTIVE:
                    i.line = i.line.strip()

            return text

        text = deleteComments(text)
        createHeader(text)
        self.txt = initMacroFunction(text, macroFunctions)
