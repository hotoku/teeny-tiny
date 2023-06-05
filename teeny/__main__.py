import sys

from .lex import *
from .parse import *


def main():
    print("Teeny Tiny Compiler")

    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1]) as fp:
        source = fp.read()

    lexer = Lexer(source)
    parser = Parser(lexer)
    parser.program()
    print("parsing completed.")


main()
