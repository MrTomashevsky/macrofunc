# модуль работы со стандартным препроцессором с++
# для работы обязательно присутствие bash и утилиты cpp в системе
import subprocess
from TmpFile import *


# true если макрос определен
def isDef(lines: list[str], macroName: str) -> bool:

    tmpInputFile1 = TmpFileCpp()
    tmpInputFile2 = TmpFileCpp()
    tmpInputFile1.writelines(lines)

    text = [f"#ifdef {macroName}\n1\n#else\n0\n#endif"]
    tmpInputFile1.writelines(text)
    cppCommand = subprocess.run(
        f"cpp -o {tmpInputFile2.name} {tmpInputFile1.name}", shell=True, capture_output=True, text=True)

    # if cppCommand.stderr != "":
    #     print(f"stderr of cpp not void: {cppCommand.stderr}")

    tailCommand = subprocess.run(
        f"tail -n 1 {tmpInputFile2.name}", shell=True, capture_output=True, text=True)

    return tailCommand.stdout[:-1] == "1"


# получить значение макроса
def value(lines: list[str], macroName: str) -> str:
    tmpInputFile1 = TmpFileCpp()
    tmpInputFile2 = TmpFileCpp()
    tmpInputFile1.writelines(lines)

    text = [f"\n\n{macroName}\n"]
    tmpInputFile1.writelines(text)

    cppCommand = subprocess.run(
        f"cpp -o {tmpInputFile2.name} {tmpInputFile1.name}", shell=True, capture_output=True, text=True)
    # assert cppCommand.stderr == "", f"stderr of cpp not void: {cppCommand.stderr}"

    # if cppCommand.stderr != "":
    #     print(f"stderr of cpp not void: {cppCommand.stderr}")

    tailCommand = subprocess.run(
        f"tail -n 1 {tmpInputFile2.name}", shell=True, capture_output=True, text=True)

    return tailCommand.stdout[:-1]
