

from MacroFunc import *


def createFunctions():
    import interp

    arr = []

    def printFunc(i):
        if index(arr, i) == -1:
            arr.append(i)
        else:
            return

        name = interp.MacroFunc.CREATE_FUNC_COMMAND(i)
        print(
            f"def {name}(self, line : LineString):\n    print(\"\\033[37;2m{name}\", str(line), \"\\033[0m\")\n\n")

    for i in interp.MacroFunc.listMacroCommand:
        printFunc(i.name)
        for j in i.endname:
            printFunc(j)


# ls = LineString(0, "##macrofunc k()")
# ind = indexDirective(ls)

# print(isBeginMacroFunc(ls))
# print(isIndexBeginMacroFunc(ind))
# print("\033[37;2m{name}\033[0m")
# createFunctions()

print(' '.isspace())

# string = """
# print("hello world!")
# print("hello world!")
# print("hello world!")
# for i in range(5):
#     print("ahahha")
# exit("pizdec")
# """
# exec(string)
