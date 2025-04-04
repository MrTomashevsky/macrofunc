

def cppGet(inputFile: str, macroName: str):
    from python_shell import Shell

    newFileName = inputFile + "_cppGetTmpFile"

    with open(inputFile, "r") as fin, open(newFileName, "w") as fout:
        fout.writelines(fin.readlines())
        fout.writelines("\n" + macroName + "\n")

    cpp = Shell.cpp(newFileName)
    print(cpp.output)


cppGet("/home/tomatik/project/kurs_proj/source/cpp.cpp", "ROW")
