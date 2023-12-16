from dataclasses import dataclass
from typing import TypeVar, Generic


Value = TypeVar("Value")


@dataclass
class ParserNode(Generic[Value]):
    value: Value
    children: list["ParserNode[Value]"]


def _start(tokens: list[str], index: int):
    t_node, t_index = _t(tokens, index)
    sum_node, new_index = _sum(tokens, t_index)
    return ParserNode("START", [t_node, sum_node]), new_index


def _sum(tokens: list[str], index: int):
    if index < len(tokens) and tokens[index] == "+":
        index += 1
        t_node, t_index = _t(tokens, index)
        sum_node, new_index = _sum(tokens, t_index)
        return ParserNode("SUM", [ParserNode("+", []), t_node, sum_node]), new_index
    else:
        return ParserNode("SUM", [ParserNode("eps", [])]), index


def _t(tokens: list[str], index: int):
    token_node, token_index = _token(tokens, index)
    prod_node, prod_index = _prod(tokens, token_index)
    return ParserNode("T", [token_node, prod_node]), prod_index


def _prod(tokens: list[str], index: int):
    if index < len(tokens) and tokens[index] == "*":
        index += 1
        token_node, token_index = _token(tokens, index)
        prod_node, new_index = _prod(tokens, token_index)
        return (
            ParserNode("PROD", [ParserNode("*", []), token_node, prod_node]),
            new_index,
        )
    else:
        return ParserNode("PROD", [ParserNode("eps", [])]), index


def _token(tokens: list[str], index: int):
    if index >= len(tokens):
        raise ValueError("incorrect index")
    if tokens[index] == "(":
        start_node, start_index = _start(tokens, index + 1)
        if tokens[start_index] == ")":
            return (
                ParserNode(
                    "TOKEN", [ParserNode("(", []), start_node, ParserNode(")", [])]
                ),
                start_index + 1,
            )
    else:
        token_node = ParserNode(f"id({tokens[index]})", [])
        return ParserNode("TOKEN", [token_node]), index + 1


def parse(tokens: list[str]) -> ParserNode[Value]:
    index = 0
    return _start(tokens, index)[0]


def pretty_print(tree: ParserNode[Value]):
    result = []

    def get_result(node, indent=0):
        result.append(("...." * indent + str(node.value)))
        for child in node.children:
            get_result(child, indent + 1)

    get_result(tree)
    print(*result, sep="\n")
