# parser.py
from typing import List
from lexer import Lexer, TokenType
from ast_nodes import Node, BinOpNode, NumNode, VarNode, AssignNode, PrintNode, CompareNode

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self) -> Node:
        token = self.current_token
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return NumNode(token.value)
        elif token.type == TokenType.ID:
            self.eat(TokenType.ID)
            return VarNode(token.value)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        self.error()

    def term(self) -> Node:
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOpNode(left=node, op=token.type, right=self.factor())
        return node

    def expr(self) -> Node:
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOpNode(left=node, op=token.type, right=self.term())
        return node

    def comparison(self) -> Node:
        node = self.expr()
        
        if self.current_token.type in (TokenType.GT, TokenType.LT, TokenType.GTE, 
                                     TokenType.LTE, TokenType.EQ, TokenType.NEQ):
            op = self.current_token.type
            self.eat(op)
            right = self.expr()
            node = CompareNode(left=node, op=op, right=right)
        
        return node

    def statement(self) -> Node:
        if self.current_token.type == TokenType.LET:
            self.eat(TokenType.LET)
            var_name = self.current_token.value
            self.eat(TokenType.ID)
            self.eat(TokenType.ASSIGN)
            expr = self.comparison()
            self.eat(TokenType.SEMI)
            return AssignNode(var=var_name, expr=expr)
        elif self.current_token.type == TokenType.PRINT:
            self.eat(TokenType.PRINT)
            self.eat(TokenType.LPAREN)
            expr = self.comparison()
            self.eat(TokenType.RPAREN)
            self.eat(TokenType.SEMI)
            return PrintNode(expr=expr)
        elif self.current_token.type == TokenType.VARS:
            self.eat(TokenType.VARS)
            self.eat(TokenType.SEMI)
            return PrintNode(expr=None)
        elif self.current_token.type == TokenType.ID:
            expr = self.comparison()
            self.eat(TokenType.SEMI)
            return PrintNode(expr=expr)
        self.error()

    def program(self) -> List[Node]:
        statements = []
        while self.current_token.type != TokenType.EOF:
            statements.append(self.statement())
        return statements
