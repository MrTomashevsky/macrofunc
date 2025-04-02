

def createFunctions():
    import interp

    arr = []

    def printFunc(i):
        global arr
        if interp.index(arr, i) == -1:
            arr.append(i)
        else:
            return

        name = interp.CREATE_FUNC_COMMAND(i)
        print(f"def {name}(self, line : LineString):\n    pass\n\n")

    for i in interp.MacroFunc.listMacroCommand:
        printFunc(i.name)
        for j in i.endname:
            printFunc(j)


# string = """
# print("hello world!")
# print("hello world!")
# print("hello world!")
# for i in range(5):
#     print("ahahha")
# exit("pizdec")
# """
# exec(string)
