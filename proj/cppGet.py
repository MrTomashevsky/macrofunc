import subprocess


def cppGet(inputFile: str, macroName: str) -> str:
    with subprocess.Popen(['pwd'], stdout=subprocess.PIPE) as pwd:
        adress = pwd.stdout.read().decode()[:len(pwd.stdout.read().decode())-1]
        with subprocess.Popen(['bash', adress + '/cpp_get.bash', inputFile, macroName], stdout=subprocess.PIPE) as proc:
            stdout = proc.stdout.read().decode()
            return stdout


def cppGetIfdef(inputFile: str, macroName: str) -> bool:
    with subprocess.Popen(['pwd'], stdout=subprocess.PIPE) as pwd:
        adress = pwd.stdout.read().decode()[:len(pwd.stdout.read().decode())-1]
        with subprocess.Popen(['bash', adress + '/cpp_get_ifdef.bash', inputFile, macroName], stdout=subprocess.PIPE) as proc:
            stdout = proc.stdout.read().decode()
            return stdout
# print(cppGet("/home/tomatik/project/kurs_proj/source/cpp.cpp", "ROW"))


print(cppGetIfdef("/home/tomatik/project/kurs_proj/cpp_tmp.cpp", "ROW"))
