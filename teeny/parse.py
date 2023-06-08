import sys
from .lex import *


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
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

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
        elif self.checkToken(TokenType.IF):
            print("STATEMENT-IF")
            self.nextToken()
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()

            while not self.checkToken(TokenType.ENDIF):
                self.statement()
            self.match(TokenType.ENDIF)
        elif self.checkToken(TokenType.WHILE):
            print("STATEMENT-WHILE")
            self.nextToken()
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()

            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
        elif self.checkToken(TokenType.LABEL):
            print("STATEMENT-LABEL")
            self.nextToken()
            self.match(TokenType.IDENT)
        elif self.checkToken(TokenType.GOTO):
            print("STATEMENT-GOTO")
            self.nextToken()
            self.match(TokenType.IDENT)
        elif self.checkToken(TokenType.LET):
            print("STATEMENT-LET")
            self.nextToken()
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)
            self.expression()
        elif self.checkToken(TokenType.INPUT):
            print("STATEMENT-INPUT")
            self.nextToken()
            self.match(TokenType.IDENT)
        else:
            self.abort(
                f"Invalid statement at {self.curToken.text} ({self.curToken.kind.name})")

        self.nl()

    def expression(self) -> None:
        print("EXPRESSION")
        self.term()
        while self.curToken.kind in (TokenType.MINUS, TokenType.PLUS):
            self.nextToken()
            self.term()

    def term(self) -> None:
        print("TERM")
        self.unary()
        while self.curToken.kind in (TokenType.SLASH, TokenType.ASTERISK):
            self.nextToken()
            self.unary()

    def unary(self) -> None:
        print("UNARY")
        if self.curToken.kind in (TokenType.PLUS, TokenType.MINUS):
            self.nextToken()
        self.primary()

    def primary(self) -> None:
        print(f"PRIMARY ({self.curToken.text})")
        if self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.IDENT):
            self.nextToken()
        else:
            self.abort(f"Expected primary at: {self.curToken.text}")

    def comparison(self) -> None:
        print("COMPARISON")

        self.expression()
        if self.isComparisonOperator():
            self.nextToken()
            self.expression()
        else:
            self.abort(
                f"Expected comparison operator at: {self.curToken.text}")

        while self.isComparisonOperator():
            self.nextToken()
            self.expression()

    def isComparisonOperator(self) -> bool:
        return self.curToken.kind in (
            TokenType.EQEQ,
            TokenType.NOTEQ,
            TokenType.GT,
            TokenType.GTEQ,
            TokenType.LT,
            TokenType.LTEQ
        )

    def nl(self) -> None:
        print("NEWLINE")
        self.match(TokenType.NEWLINE)
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
