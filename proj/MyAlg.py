
def index(line, what):
    try:
        return line.index(what)
    except ValueError:
        return -1


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

    for value in returnValue:
        value = value.strip()

    assert countNoClosedRoundBracket == 0, "not closed round bracket " + args
    assert countNoClosedQuotes == False, "not closed quotes"

    return returnValue


def getStripArgs(line: str):
    args = getArgs(line[1:len(line)-1])
    return [i.strip() for i in args]
