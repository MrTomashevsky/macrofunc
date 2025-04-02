

def createFunctions():
    import interp

    arr = []

    def printFunc(i):
        if interp.index(arr, i) == -1:
            arr.append(i)
        else:
            return

        name = interp.MacroFunc.CREATE_FUNC_COMMAND(i)
        print(f"def {name}(self, line : LineString):\n    pass\n\n")

    for i in interp.MacroFunc.listMacroCommand:
        printFunc(i.name)
        for j in i.endname:
            printFunc(j)


createFunctions()

# string = """
# print("hello world!")
# print("hello world!")
# print("hello world!")
# for i in range(5):
#     print("ahahha")
# exit("pizdec")
# """
# exec(string)
