# обработчик команд из командной строки
from clah2 import *
import sys
import os


class PrimitiveType:
    # тип - одна строка
    @staticmethod
    def STRING(args: list, argv):
        args.append(argv[0])
        return 1

    # тип - адрес файла
    @staticmethod
    def FILE(args: list, argv):
        assert os.path.isfile(argv[0]), f"it's not file {argv[0]}"
        args.append(argv[0])
        return 1

    # тип - одно число integer
    @staticmethod
    def INT(args: list, argv):
        args.append(int(argv[0]))
        return 1

    # тип - одно число float
    @staticmethod
    def FLOAT(args: list, argv):
        args.append(float(argv[0]))
        return 1


# класс типа аргумента
# имена функций использовать так, будто они элементы Enum
class Type(PrimitiveType):
    # тип - массив строк (данный тип всегда будет последним
    # в массиве типов, так как под массивом строк понимаются
    # вообще все строки с индекса этого типа в массиве типов
    # вплоть до конца argv)
    @staticmethod
    def ARRAY_STRINGS(args: list, argv):
        for i in argv:
            args.append(i)
        return len(argv)


# класс ключей
# ключ - это то же самое что подкоманда, но у него количество аргументов фиксированно
# ключ не может иметь ключей или подкоманд, не может принимать на вход массив строк
# ключи считывааются перед считыванием аргументов и подкоманд
# ключи бывают короткие - тире и одна буква, например -f -k -l, - и длинные - --one-file, --substring и т.д.
# для ключа можно задать и короткое и длинное имя
class Key:
    nameLong: str
    nameShort: str
    types: list[PrimitiveType]
    function: None

    def __init__(self, nameLong: str,  nameShort: str, types: list[PrimitiveType], function):
        self.nameLong, self.nameShort, self.types, self.function = nameLong, nameShort, types, function

    def __call__(self, argv) -> int:
        functionArgs = []
        for i in range(len(self.types)):
            self.types[i](functionArgs, argv[i:])
        if self.function != None:
            self.function(functionArgs)
        return len(self.types)


# поиск ключа в массиве ключей по названию
def indexKey(arg: str, keys: list[Key]) -> int:
    isLong: bool

    if len(arg) >= 2 and arg[0] == arg[1] == '-':
        arg = arg[2:]
        isLong = True
    elif len(arg) >= 1 and arg[0] == '-':
        arg = arg[1:]
        isLong = False
    else:
        return -1

    for index, key in enumerate(keys):
        if isLong:
            if arg == key.nameLong:
                return index
        else:
            if arg == key.nameShort:
                return index

    return -1


class Command:
    pass


# поиск команды в массиве команд по названию
def indexCommand(arg: str, commands: list[Command]):
    for index, command in enumerate(commands):
        if arg == command.name:
            return index
    return -1


# класс команды - основной класс
# для создания обработчика аргументов командной строки основную программу нужно определить как команду
# (смотри пример ниже)
#
# также этот класс используется для представления подкоманд
# у команды могут быть ключи (необязательный параметр), аргументы и подкоманды
# сначала считываются ключи (если есть)
# после ищутся подкоманды - если найдена, то обработка подкоманды
# лишь если не найдены подкоманды, начинается интерпретация аргументов
class Command:
    name: str
    keys: list[Key]
    types: list[Type]
    commands: list[Command]
    function: None

    def __init__(self, name: str, keys: list[Key], types: list[Type], commands: list[Command], function):
        self.name, self.keys, self.types, self.commands, self.function = name, keys, types, commands, function

    def __call__(self, argv):
        readArguments = False
        functionArgs = []
        i = 0
        while i < len(argv):
            ind = indexKey(argv[i], self.keys)
            if ind != -1:
                i += 1
                i += self.keys[ind](argv[i:])
            else:
                ind = indexCommand(argv[i], self.commands)
                readArguments = True
                if ind != -1:
                    i += self.commands[ind](argv[i+1:])
                    i += 1
                    argv = []
                else:
                    indexType = 0
                    while i < len(argv) and indexType < len(self.types):
                        i += self.types[indexType](functionArgs, argv[i:])
                        indexType += 1
                    assert indexType == len(self.types) and i == len(
                        argv), f"'{self.name}({argv})': the number of specified arguments is not equal to the amount of expected"

        if (len(self.types) != 0):
            error: str
            if self.name == None:
                error = "no arguments for command"
            else:
                error = f"no arguments for '{self.name}'"
            assert readArguments, error

        if self.function != None:
            self.function(functionArgs)
        return i

# # пример:

# from clah2 import *

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


# def main_output(args: list):
#     print('main_output', args)


# def output(args: list):
#     print('output', args)


# def output2(args: list):
#     print('output2', args)


# main = Command(
#     "main",
#     [Key(None, "o", [PrimitiveType.FILE], output)],
#     [],
#     [
#         Command("work", [Key(None, "o", [PrimitiveType.FLOAT, PrimitiveType.FLOAT], output2)], [
#                 Type.INT, Type.INT], [], work),
#         Command("array", [], [Type.ARRAY_STRINGS], [], array),
#         Command("hello", [], [], [], hello),
#         Command("string", [], [Type.STRING], [], string),
#         Command("command", [], [], [
#             Command("file", [], [Type.FILE], [], file),
#             Command("error", [], [], [], error),
#         ], None)
#     ],
#     None
# )

# main(["-o", "/home/tomatik/project/python/tgbot/m.py",
#      "work", "-o", "212", "344", "12", "23222"])
