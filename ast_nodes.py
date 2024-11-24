# ast_nodes.py
from dataclasses import dataclass
from typing import Any
from lexer import TokenType

@dataclass
class Node:
    pass

@dataclass
class BinOpNode(Node):
    left: Node
    op: TokenType
    right: Node

@dataclass
class NumNode(Node):
    value: str

@dataclass
class VarNode(Node):
    name: str

@dataclass
class AssignNode(Node):
    var: str
    expr: Node

@dataclass
class PrintNode(Node):
    expr: Node

@dataclass
class CompareNode(Node):
    left: Node
    op: TokenType
    right: Node