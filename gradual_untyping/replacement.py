from typing import NamedTuple


class Replacement(NamedTuple):
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    type: str

    def __lt__(self, other):
        return self[:2] < other[:2]
