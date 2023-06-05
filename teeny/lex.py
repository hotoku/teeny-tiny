import enum
import sys
from typing import Optional


class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Token:
    def __init__(self, tokenText: str, tokenKind: TokenType) -> None:
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def checkIfKeyword(tokenText: str) -> Optional[TokenType]:
        for kind in TokenType:
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200:
                return kind
        return None


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source
        self.curChar = ""
        self.curPos = -1
        self.nextChar()

    def nextChar(self) -> None:
        """1文字読み込む。

        この関数自体は、値を返さず、メンバー変数curChar(=現在着目している文字)に副作用を起こすだけ。
        現在の文字がほしい場合は、self.curCharにアクセスする。
        現在の文字への参照は複数回、色んな場所からあるかもしれない想定。

        この関数が呼ばれる = 呼ばれる前のcurPos, curCharが消費され、次の文字に着目する状態になる。
        """
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = "\0"
        else:
            self.curChar = self.source[self.curPos]

    def peek(self) -> str:
        """内部状態を変更せずに、次の文字を返す
        """
        if self.curPos + 1 >= len(self.source):
            return "\0"
        else:
            return self.source[self.curPos + 1]

    def abort(self, message: str) -> None:
        sys.exit("Lexing error. " + message)

    def skipWhitespace(self) -> None:
        while self.curChar in " \t\r":
            self.nextChar()

    def skipComment(self) -> None:
        if self.curChar == "#":
            while self.curChar != "\n":
                self.nextChar()

    def getToken(self) -> Token:
        self.skipWhitespace()
        self.skipComment()
        token = None
        if self.curChar == "+":
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == "-":
            token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == "*":
            token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "/":
            token = Token(self.curChar, TokenType.SLASH)
        elif self.curChar == "\n":
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == "\0":
            token = Token(self.curChar, TokenType.EOF)
        elif self.curChar == "=":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.EQEQ)
            else:
                token = Token(self.curChar, TokenType.EQ)
        elif self.curChar == ">":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.GTEQ)
            else:
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == "<":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.LTEQ)
            else:
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == "!":
            if self.peek() == "=":
                lastChar = self.curChar
                self.nextChar()
                token = Token(lastChar + self.curChar, TokenType.NOTEQ)
            else:
                self.abort("Expected !=, got !" + self.peek())
                assert False
        elif self.curChar == '"':
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '"':
                if self.curChar in "\r\n\t\\%":
                    self.abort(
                        f"Illegal Character in string. {self.curChar}@{self.curPos}")
                    assert False
                self.nextChar()
            tokText = self.source[startPos: self.curPos]
            token = Token(tokText, TokenType.STRING)
        elif self.curChar.isdigit():
            startPos = self.curPos
            while self.peek().isdigit():
                self.nextChar()
            if self.peek() == ".":
                self.nextChar()
                if not self.peek().isdigit():
                    self.abort(
                        f"Illegal character in number. {self.curChar}@{self.curPos}")
                    assert False
                while self.peek().isdigit():
                    self.nextChar()
            tokText = self.source[startPos:self.curPos + 1]
            token = Token(tokText, TokenType.NUMBER)
        elif self.curChar.isalpha():
            startPos = self.curPos
            while self.peek().isalnum():
                self.nextChar()
            tokText = self.source[startPos:self.curPos + 1]
            keyword = Token.checkIfKeyword(tokText)
            if keyword == None:
                token = Token(tokText, TokenType.IDENT)
            else:
                token = Token(tokText, keyword)
        else:
            self.abort(f"Unknown token: {self.curChar}@{self.curPos}")
            assert False

        # ここの時点で、内部状態は、現在のトークンの最後の文字に着目している状態。
        # リターンの直前で、ここまでの結果を消費し、次の読み込みに備える。
        self.nextChar()
        return token
