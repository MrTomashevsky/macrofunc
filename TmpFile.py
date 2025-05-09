from tempfile import NamedTemporaryFile


class TmpFileCpp:
    TF: None
    name: str

    def __init__(self):
        self.TF = NamedTemporaryFile("w+t", suffix='.cpp', delete=True)
        self.name = self.TF.name

    def writelines(self, lines):
        self.TF.writelines(lines)
        self.TF.flush()

    def clear(self):
        self.TF.truncate(0)

    def delete(self):
        self.clear()
        self.TF.close()
