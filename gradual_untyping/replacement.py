from typing import NamedTuple


class Replacement(NamedTuple):
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    replace_with: str
    mark: str

    @classmethod
    def from_node(cls, node, mark=""):
        return cls(
            node.lineno - 1,
            node.col_offset,
            node.end_lineno - 1,
            node.end_col_offset,
            getattr(node, "replace_with", ""),
            mark,
        )
