from clah import Command, Type, Argument, commandLineAgrumentHandler
import sys
import interp

argv = ["create",
        "/home/tomatik/project/kurs_proj/source/cpp.cpp",
        "/home/tomatik/project/kurs_proj/source/cpp2.cpp"
        ]  # sys.argv[1:]


# argv = ["create",
#         "/home/tomatik/project/kurs_proj/source/cppMacro.cpp",
#         "/home/tomatik/project/kurs_proj/source/cppMacro2.cpp"
#         ]  # sys.argv[1:]


def create(args: list):
    interp.interp(args[0], args[1])


def help(args: list):
    print('help', args)


commands = [
    Command("--help", [], help),
    Command("create", [Argument(Type.FILE), Argument(Type.FILE)], create)
]

# /bin/python /home/tomatik/project/kurs_proj/proj/main.py create /home/tomatik/project/kurs_proj/source/cpp.cpp /home/tomatik/project/kurs_proj/source/cpp2.cpp


# try:
commandLineAgrumentHandler(argv, commands)
# except Exception as ex:
#     print(ex)
