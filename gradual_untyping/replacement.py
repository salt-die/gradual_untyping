import ast
from typing import NamedTuple


class Replacement(NamedTuple):
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    source: str
    type: type
    replace_with: str=""

    @classmethod
    def from_node(cls, node, type, source):
        return cls(
            node.lineno - 1,
            node.col_offset,
            node.end_lineno - 1,
            node.end_col_offset,
            ast.get_source_segment(source, node),
            type,
            getattr(node, "replace_with", ""),
        )
