# interpreter.py
from typing import List, Optional
from lexer import TokenType
from ast_nodes import Node, BinOpNode, NumNode, VarNode, AssignNode, PrintNode, CompareNode

class Interpreter:
    def __init__(self):
        self.variables = {}

    def visit_BinOpNode(self, node: BinOpNode) -> float:
        if node.op == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_NumNode(self, node: NumNode) -> float:
        return float(node.value)

    def visit_VarNode(self, node: VarNode) -> float:
        if node.name not in self.variables:
            raise Exception(f'Undefined variable: {node.name}')
        return self.variables[node.name]

    def visit_AssignNode(self, node: AssignNode):
        self.variables[node.var] = self.visit(node.expr)

    def visit_PrintNode(self, node: PrintNode):
        if node.expr is None:  # vars command
            if not self.variables:
                print("No variables defined")
                return
            print("\nCurrent variables:")
            max_len = max(len(name) for name in self.variables)
            for name in sorted(self.variables):
                print(f"{name:<{max_len}} = {self.variables[name]}")
            return
            
        value = self.visit(node.expr)
        print(value)

    def visit_CompareNode(self, node: CompareNode) -> float:
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op == TokenType.GT:
            return float(left > right)
        elif node.op == TokenType.LT:
            return float(left < right)
        elif node.op == TokenType.GTE:
            return float(left >= right)
        elif node.op == TokenType.LTE:
            return float(left <= right)
        elif node.op == TokenType.EQ:
            return float(left == right)
        elif node.op == TokenType.NEQ:
            return float(left != right)

    def visit(self, node: Node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)

    def interpret(self, nodes: List[Node]):
        for node in nodes:
            self.visit(node)