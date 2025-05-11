import enum

# ConditionEnum = enum.Enum(names=('IF ELIF ELSE'))


class ConditionsInfo:
    was: bool
    value: bool

    def __init__(self, was: bool, value: bool):
        self.was, self.value = was, value

    def __str__(self):
        return f"{self.was}, {self.value}"


class ConditionsSearch:
    viewedConditions: list[dict[str, ]]

    def _push_null(self):
        self.viewedConditions.append({
            "if": ConditionsInfo(False, False),
            "elif": ConditionsInfo(False, False),
            "else": False
        })

    def printer(self):
        for ind, i in enumerate(self.viewedConditions):
            print(f"[{ind}]")
            for j in i:
                print(f"{j} = {i[j]}")

    def __init__(self):
        self.viewedConditions = []
        self._push_null()

    def ifAllConditionsExit(self):
        for i in self.viewedConditions[-1]:
            if not self.viewedConditions[-1][i].was:
                return
        self.viewedConditions = self.viewedConditions[:-1]
        self.printer()

    def pushIf(self, value) -> bool:
        if self.viewedConditions[-1]["if"].was:
            self._push_null()
        self.viewedConditions[-1]["if"].was = True
        self.viewedConditions[-1]["if"].value = value
        self.printer()
        return value

    def pushElif(self, value) -> bool:
        assert self.viewedConditions[-1]["if"].was, "'elif' must be after 'if', but 'if' not find"
        assert not self.viewedConditions[-1]["else"], "'elif' after 'else'"
        self.viewedConditions[-1]["elif"].was = True
        self.viewedConditions[-1]["if"].value = value
        self.printer()
        return value

    def pushElse(self) -> bool:
        assert self.viewedConditions[-1]["if"].was, "'else' must be after 'if', but 'if' not find"
        assert not self.viewedConditions[-1]["else"], "too many teams 'else'"
        self.viewedConditions[-1]["else"] = True
        self.printer()

    def pushEndif(self):
        assert self.viewedConditions[-1]["if"], "'endif' must be after 'if', but 'if' not find"
        self.viewedConditions = self.viewedConditions[:-1]
        self.printer()

    def __del__(self):
        assert len(self.viewedConditions) == 1 and self.viewedConditions[0][
            "if"].was == self.viewedConditions[0]["endif"].was, "not closed visible area 'if'"


def printer(value):
    print(f"<{value}>\n\n")


def fun1():
    cs = ConditionsSearch()

    printer(cs.pushIf(False))
    printer(cs.pushIf(False))

    # input("pause")


fun1()
