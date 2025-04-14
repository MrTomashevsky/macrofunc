# обработчик команд из командной строки
import os


class Command:
    pass


# функция обработчика
def commandLineAgrumentHandler(argv: list[str], commands: list[Command]):
    assert len(argv) != 0, "no args"

    for command in commands:
        if argv[0] == command.name:
            command(argv[1:], commands)
            return

    raise Exception(f"{argv[0]} - unkwnown command")


# класс типа аргумента
# имена функций использовать так, будто они элементы Enum
class Type:
    # тип - одна строка
    @staticmethod
    def STRING(args: list, argv, commands):
        args.append(argv[0])
        return 1

    # тип - адрес файла
    @staticmethod
    def FILE(args: list, argv, commands):
        assert os.path.isfile(argv[0]), f"it's not file {argv[0]}"
        args.append(argv[0])
        return 1

    # тип - одно число integer

    @staticmethod
    def INT(args: list, argv, commands):
        args.append(int(argv[0]))
        return 1

    # тип - массив строк (данный тип всегда будет последним
    # в массиве типов, так как под массивом строк понимаются
    # вообще все строки с индекса этого типа в массиве типов
    # вплоть до конца argv)
    @staticmethod
    def ARRAY_STRINGS(args: list, argv, commands):
        for i in argv:
            args.append(i)
        return len(argv)

    # тип - команда (например, у команды apt в Linux Debian
    # в таком случае командами является install, update и т.д.)
    # тут ситуация такая же, как и с массивом строк - точно также
    # это гарантировано последний тип в массиве типов
    @staticmethod
    def COMMAND(args: list, argv, commands):
        args.append(commandLineAgrumentHandler(argv, commands))
        return len(argv)


# класс аргумента: хранит его ожидаемый тип и массив команд
# (массив необходим только в том случае, если type == Type.COMMAND)
class Argument:
    type: Type
    commands: list[Command]

    def __init__(self, type, commands=[]):
        self.type, self.commands = type, commands


# класс команды: имя, массивов типов, указатель на функцию исполнения
class Command:
    name: str
    argsTypes: list[Argument]
    function: None

    def __init__(self, name, argsTypes, function=None):
        self.name, self.argsTypes, self.function = name, argsTypes, function

    # исполнение команды
    def __call__(self, argv, commands):
        args = []
        i = 0
        for obj in self.argsTypes:
            stringArgument: str
            if i >= len(argv):
                stringArgument = [""]
            else:
                stringArgument = argv[i:]

            i += obj.type(args, stringArgument, obj.commands)

        assert i == len(argv), f"unknown arguments in command '{self.name}'"

        if self.function != None:
            self.function(args)


# # пример:

# from clah import Command, Type, Argument, commandLineAgrumentHandler
# import sys

# def work(args: list):
#     print('work', args)


# def array(args: list):
#     print('array', args)


# def hello(args: list):
#     print('hello', args)


# def string(args: list):
#     print('string', args)


# def command(args: list):
#     print('command', args)


# def file(args: list):
#     print('file', args)


# def error(args: list):
#     print('error', args)


# commands = [
#     Command("work", [Argument(Type.INT)], work),
#     Command("array", [Argument(Type.ARRAY_STRINGS)], array),
#     Command("hello", [], hello),
#     Command("string", [Argument(Type.STRING)], string),
#     Command("command", [Argument(Type.COMMAND, [
#         Command("file", [Argument(Type.FILE)], file),
#         Command("error", [], error),
#     ])])
# ]

# commandLineAgrumentHandler(
#     ["command", "error"], commands)
