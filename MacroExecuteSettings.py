# модуль обработчиков областей видимости, условий и циклов

# класс области видимости условий
class IfElseInfo:
    pIf = False
    pElif = False
    pElse = False
    correctSolutionWasFound = False
    canExecute = False


# класс обработчик областей видимости
class ConditionsSearch:
    viewedConditions: list[IfElseInfo] = [IfElseInfo()]

    def pushIf(self, value):
        if self.viewedConditions[-1].pIf:
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
        return self.viewedConditions[-1].canExecute

    def __del__(self):
        assert len(
            self.viewedConditions) == 0, f"not closed visible area 'if': {len(self.viewedConditions)}"
