import subprocess

CPP_GET = "/home/tomatik/project/kurs_proj/script/cpp_get.bash"
CPP_GET_IFDEF = "/home/tomatik/project/kurs_proj/script/cpp_get_ifdef.bash"


def value(inputFile: str, macroName: str) -> str:
    with subprocess.Popen(['bash', CPP_GET, inputFile, macroName], stdout=subprocess.PIPE) as proc:
        stdout = proc.stdout.read().decode()
        return stdout


def isDef(inputFile: str, macroName: str) -> bool:
    with subprocess.Popen(['bash', CPP_GET_IFDEF, inputFile, macroName], stdout=subprocess.PIPE) as proc:
        stdout = proc.stdout.read().decode()
        return stdout == "\n1\n"


# print(cppGetIfdef("/home/tomatik/project/kurs_proj/source/cpp_tmp.cpp", "__cplusplus"))
