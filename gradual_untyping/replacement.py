from typing import NamedTuple


class Replacement(NamedTuple):
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    replace_with: str
    mark: str | bool
    include_mark: bool

    @classmethod
    def from_node(cls, node, mark=False, delete_mark=False):
        return cls(
            node.lineno - 1,
            node.col_offset,
            node.end_lineno - 1,
            node.end_col_offset,
            getattr(node, "replace_with", ""),
            mark,
            delete_mark,
        )
