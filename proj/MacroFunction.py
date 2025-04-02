import MacroFunc
import cpp_comments
from MacroFunc import LineString, TextMacroFunction
from MyAlg import *

type ListMacroFunction = list[MacroFunction]


def initMacroFunction(text: TextMacroFunction, macroFunctions: ListMacroFunction):
    assert MacroFunc.isBeginMacroFunc(text[0])
    assert MacroFunc.isEndMacroFunc(text[len(text)-1])

    text = text[1:len(text)-1]
    text = [i for i in text if not i.line.strip() == ""]

    for i in text:
        if MacroFunc.isDirective(i):
            i.line = i.line.strip()

    return text


class MacroFunction:
    name: str = ""
    args: list[str] = []
    txt: TextMacroFunction = []

    def __str__(self):
        returnValue = self.name + str(self.args) + "\n"
        for j in self.txt:
            returnValue = returnValue + str(j) + "\n"
        return returnValue

    def __init__(self, text: TextMacroFunction, macroFunctions: ListMacroFunction):
        def createHeader(text):
            line = text[0]
            self.name, args = MacroFunc.getNameAndArgsMacroCommand(line)
            self.args = getArgs(args)

        def deleteComments(text):
            tmptext = []
            isMultiLineComment = False
            ind: int
            for i in text:
                line = i.line

                if isMultiLineComment:
                    ind = cpp_comments.indexEndMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = False
                        line = line[ind+len(MacroFunc.BEGIN_COMMAND):]
                    else:
                        line = ""
                else:
                    ind = cpp_comments.indexBeginMultiLineComment(i.line)
                    if ind != -1:
                        isMultiLineComment = True
                        line = line[:ind]

                ind = cpp_comments.indexSingleLineComment(i.line)
                if ind != -1:
                    line = line[:ind]

                tmptext.append(LineString(i.numb, line))

            return tmptext

        text = deleteComments(text)
        createHeader(text)
        self.txt = initMacroFunction(text, macroFunctions)
