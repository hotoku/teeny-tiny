class Emitter:
    def __init__(self, fullPath: str) -> None:
        self.fullPath = fullPath
        self.header = ""
        self.code = ""

    def emit(self, code: str) -> None:
        self.code += code

    def emitLine(self, code: str) -> None:
        self.code += code + "\n"

    def headerLIne(self, code: str) -> None:
        self.header += code + "\n"

    def writeFile(self) -> None:
        with open(self.fullPath, "w") as of:
            of.write(self.header + self.code)
