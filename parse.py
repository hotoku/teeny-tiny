import sys
from lex import *


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer

        self.curToken: Token = None  # type: ignore
        self.peekToken: Token = None  # type: ignore
        self.nextToken()
        self.nextToken()

    def checkToken(self, kind: TokenType) -> bool:
        return kind == self.curToken.kind

    def checkPeek(self, kind: TokenType) -> bool:
        return kind == self.peekToken.kind

    def match(self, kind: TokenType) -> None:
        """現在のトークンが、特定のタイプであるかをチェックする。

        チェックに通らない場合、文法エラーを投げて終了。
        チェックに通る場合、1トークンを消費する(内部状態を次に進める)。
        """
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name +
                       ", got " + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self) -> None:
        """内部状態を、1トークン進める"""
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message: str) -> None:
        sys.exit("Error. " + message)

    def program(self) -> None:
        print("PROGRAM")
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self) -> None:
        if self.checkToken(TokenType.PRINT):
            print("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                self.nextToken()
            else:
                self.expression()

        self.nl()

    def nl(self) -> None:
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
