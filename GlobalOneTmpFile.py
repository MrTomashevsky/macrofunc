from tempfile import NamedTemporaryFile

# Инициализация при первом импорте
TF = NamedTemporaryFile(suffix='.cpp', delete=True)
name = TF.name


def init(lines):
    TF.writelines(lines)
    TF.flush()


def clear():
    TF.truncate(0)


def del_resources():
    clear()
    TF.close()
