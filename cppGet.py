# модуль работы со стандартным препроцессором с++
# для работы обязательно присутствие bash и утилиты cpp в системе

import subprocess

# расположение bash-скриптов
CPP_GET = "script/cpp_get.bash"
CPP_GET_IFDEF = "script/cpp_get_ifdef.bash"


# получить значение макроса
def value(inputFile: str, macroName: str) -> str:
    with subprocess.Popen(['bash', CPP_GET, inputFile, macroName], stdout=subprocess.PIPE) as proc:
        stdout = proc.stdout.read().decode()
        return stdout


# true если макрос определен
def isDef(inputFile: str, macroName: str) -> bool:
    with subprocess.Popen(['bash', CPP_GET_IFDEF, inputFile, macroName], stdout=subprocess.PIPE) as proc:
        stdout = proc.stdout.read().decode()
        return stdout == "\n1\n"
