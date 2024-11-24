# lexer.py
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class TokenType(Enum):
    NUMBER = 'NUMBER'
    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MUL = 'MUL'
    DIV = 'DIV'
    ID = 'ID'
    ASSIGN = 'ASSIGN'
    SEMI = 'SEMI'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LET = 'LET'
    PRINT = 'PRINT'
    VARS = 'VARS'
    GT = 'GT'
    LT = 'LT'
    GTE = 'GTE'
    LTE = 'LTE'
    EQ = 'EQ'
    NEQ = 'NEQ'
    EOF = 'EOF'

@dataclass
class Token:
    type: TokenType
    value: Optional[str] = None

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if text else None

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def number(self) -> Token:
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return Token(TokenType.NUMBER, result)

    def identifier(self) -> Token:
        result = ''
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        if result == 'let':
            return Token(TokenType.LET)
        elif result == 'print':
            return Token(TokenType.PRINT)
        elif result == 'vars':
            return Token(TokenType.VARS)
        return Token(TokenType.ID, result)

    def get_next_token(self) -> Token:
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha():
                return self.identifier()

            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.EQ)
                return Token(TokenType.ASSIGN)

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.GTE)
                return Token(TokenType.GT)

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.LTE)
                return Token(TokenType.LT)

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(TokenType.NEQ)
                self.error()

            if self.current_char == ';':
                self.advance()
                return Token(TokenType.SEMI)

            if self.current_char == '+':
                self.advance()
                return Token(TokenType.PLUS)

            if self.current_char == '-':
                self.advance()
                return Token(TokenType.MINUS)

            if self.current_char == '*':
                self.advance()
                return Token(TokenType.MUL)

            if self.current_char == '/':
                self.advance()
                return Token(TokenType.DIV)

            if self.current_char == '(':
                self.advance()
                return Token(TokenType.LPAREN)

            if self.current_char == ')':
                self.advance()
                return Token(TokenType.RPAREN)

            self.error()

        return Token(TokenType.EOF)