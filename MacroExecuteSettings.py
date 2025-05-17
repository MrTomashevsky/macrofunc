# модуль обработчиков областей видимости, условий и циклов
from MyAlg import *


# класс области видимости условий
class IfElseInfo:
    pIf = False
    pElif = False
    pElse = False
    correctSolutionWasFound = False
    canExecute = False


# класс обработчик областей видимости
class ConditionsSaver:
    viewedConditions: list[IfElseInfo] = []

    def pushIf(self, value):
        if len(self.viewedConditions) == 0 or self.viewedConditions[-1].pIf:
            self.viewedConditions.append(IfElseInfo())
        self.viewedConditions[-1].pIf = True

        if value:
            self.viewedConditions[-1].correctSolutionWasFound = True
            self.viewedConditions[-1].canExecute = True

    def pushElif(self, value):
        assert self.viewedConditions[-1].pIf, "'elif' must be after 'if', but 'if' not find"
        assert not self.viewedConditions[-1].pElse, "'elif' after 'else'"

        self.viewedConditions[-1].pElif = True

        if value and not self.viewedConditions[-1].correctSolutionWasFound:
            self.viewedConditions[-1].correctSolutionWasFound = True
            self.viewedConditions[-1].canExecute = True
        else:
            self.viewedConditions[-1].canExecute = False

    def pushElse(self) -> bool:
        assert self.viewedConditions[-1].pIf, "'else' must be after 'if', but 'if' not find"
        assert not self.viewedConditions[-1].pElse, "too many teams 'else'"

        self.viewedConditions[-1].pElse = True

        if not self.viewedConditions[-1].correctSolutionWasFound:
            self.viewedConditions[-1].correctSolutionWasFound = True
            self.viewedConditions[-1].canExecute = True
        else:
            self.viewedConditions[-1].canExecute = False

    def pushEndif(self):
        assert self.viewedConditions[-1].pIf, "'endif' must be after 'if', but 'if' not find"
        self.viewedConditions = self.viewedConditions[:-1]

    # находится ли текущая команда в области видимости верного условия?
    def canExecute(self) -> bool:
        if len(self.viewedConditions) == 0:
            return True
        return self.viewedConditions[-1].canExecute

    def __del__(self):
        assert len(
            self.viewedConditions) == 0, f"not closed visible area 'if': {len(self.viewedConditions)}"


class ForInfo:
    indexFor: int
    indexEndFor: int

    def __init__(self, indexFor: int, indexEndFor: int):
        self.indexFor, self.indexEndFor = indexFor, indexEndFor


class CicleSaver:
    viewedCircles: list[ForInfo] = []
    _canExecute: bool = True
    counterFor: int = 0

    def findFor(self, thisIndex) -> int:
        for i, obj in enumerate(self.viewedCircles):
            if obj.indexFor == thisIndex:
                return i
        return -1

    def findEndFor(self, thisIndex) -> int:
        for i, obj in enumerate(self.viewedCircles):
            if obj.indexEndFor == thisIndex:
                return i
        return -1

    def declareFor(self, thisIndex) -> ForInfo:
        if len(self.viewedCircles) == 0 or isIndex(self.viewedCircles[-1].indexFor):
            self.viewedCircles.append(ForInfo(thisIndex, -1))
        return self.viewedCircles[-1]

    def setCanExecute(self):
        self._canExecute = True

    def resetCanExecute(self):
        self._canExecute = False

    def updateFor(self, indexEndFor: int):
        assert len(self.viewedCircles) != 0, "unknown 'endfor'"
        assert isIndex(
            self.viewedCircles[-1].indexFor), "'endfor' must be after 'for', but 'for' not find"
        assert not isIndex(
            self.viewedCircles[-1].indexEndFor), "'endfor' must be after 'for', but 'for' not with 'endfor' not find"
        self.viewedCircles[-1].indexEndFor = indexEndFor

    def lastFor(self) -> ForInfo:
        return self.viewedCircles[-1]

    def deleteLastFor(self):
        self.viewedCircles = self.viewedCircles[:-1]

    def canExecute(self) -> bool:
        return self._canExecute

    def __del__(self):
        assert len(
            self.viewedCircles) == 0, f"not closed visible area 'cicle': {len(self.viewedCircles)}"
