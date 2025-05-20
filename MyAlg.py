# модуль некоторых алгоритмов, которые используются во всех или в большинстве файлов проекта


# индекс может быть только положительным
def isIndex(dig):
    return dig >= 0


# получить индекс элоемента в массиве; -1 если не найден
def index(line, what):
    try:
        return line.index(what)
    except ValueError:
        return -1


# парсинг аргументов из строки вида "arg1, arg2, arg3" и тд
# нуждается в дополнительном тестировании
def getArgs(args: str) -> list[str]:
    returnValue: list[str] = []
    countNoClosedRoundBracket = 0
    countNoClosedQuotes = False

    for charaster in args:

        if countNoClosedRoundBracket == 0 and countNoClosedQuotes == False and charaster == ",":
            returnValue.append("")
        else:
            if len(returnValue) == 0:
                returnValue.append(charaster)
            else:
                returnValue[len(returnValue)-1] += charaster

        if charaster == "\\":
            pass

        if charaster == "\"":

            if returnValue[len(returnValue)-1][len(returnValue[len(returnValue)-1])-2] == "\\":
                returnValue[len(returnValue) - 1] = returnValue[len(returnValue) -
                                                                1][:len(returnValue[len(returnValue)-1])-2]

                returnValue[len(returnValue)-1] += "\""
            else:
                countNoClosedQuotes = not countNoClosedQuotes

        if countNoClosedQuotes == False:
            if charaster == "(":
                countNoClosedRoundBracket += 1
            elif charaster == ")":
                countNoClosedRoundBracket -= 1

    returnValue = [value.strip() for value in returnValue]

    assert countNoClosedRoundBracket == 0, "not closed round bracket " + args
    assert countNoClosedQuotes == False, "not closed quotes"

    return returnValue


def getStripArgs(line: str):
    args = getArgs(line[1:len(line)-1])
    return [i.strip() for i in args]


def delete2Charp(line: str):
    def lastAlNumLowUnderlin(line: str, start: int = 0, end: int = -1):
        if end == -1:
            end = len(line)
        for i in range(end, start, -1):
            if line[i].isalnum() or line[i] == "_":
                return i
        return start

    def firstAlNumLowUnderlin(line: str, start: int = 0, end: int = -1):
        if end == -1:
            end = len(line)
        for i in range(start, end):
            if line[i].isalnum() or line[i] == "_":
                return i
        return end

    while True:
        ind = index(line, "##")
        if ind == -1:
            break
        lastInd = lastAlNumLowUnderlin(line, 0, ind)+1
        firstInd = firstAlNumLowUnderlin(line, ind + 2, -1)

        line = line[:lastInd] + line[firstInd:]
    return line


def inListPermissibleCharasters(symb: str) -> bool:
    return not symb.isalnum() and not symb.isspace()


def findWord(line: str, startIndex: int, what: str) -> int:
    while True:
        try:
            startIndex = line.index(what, startIndex)
            fw, lw = True, True
            if startIndex > 0:
                fw = line[startIndex -
                          1].isspace() or inListPermissibleCharasters(line[startIndex-1])
            if startIndex + len(what) < len(line) - 1:
                lw = line[startIndex +
                          len(what)].isspace() or inListPermissibleCharasters(line[startIndex + len(what)])
            if fw and lw:
                return startIndex
            startIndex += len(what)
        except ValueError:
            return -1


def findFunction(line: str, startIndex: int, what: str) -> int:
    while True:
        try:
            startIndex = line.index(what, startIndex)
            fw, lw = True, True
            if startIndex > 0:
                fw = line[startIndex -
                          1].isspace() or inListPermissibleCharasters(line[startIndex-1])
            if startIndex + len(what) < len(line) - 1:
                lw = line[startIndex + len(what)] == "("
            if fw and lw:
                return startIndex
            startIndex += len(what)
        except ValueError:
            return -1

# def findIndexesWords(line: str, what: str) -> list[int]:
#     result: list[int] = []
#     tmpIndex = 0
#     while True:
#         try:
#             tmpIndex = line.index(what, tmpIndex)
#             fw, lw = True, True
#             if tmpIndex > 0:
#                 fw = line[tmpIndex-1].isspace() or line[tmpIndex-1] == "#"
#             if tmpIndex + len(what) < len(line) - 1:
#                 lw = line[tmpIndex +
#                           len(what)].isspace() or line[tmpIndex + len(what)] == "#"
#             if fw and lw:
#                 result.append(tmpIndex)
#             tmpIndex += len(what)
#         except ValueError:
#             break
#     return result
# print(findIndexesWords(
#     "sizeof sizeof()#sizeof#sizeof assizeof sizeofl 1sizeof0", "sizeof"))
