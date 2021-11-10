from typing import NamedTuple


class Replacement(NamedTuple):
    lineno: int
    col_offset: int
    end_lineno: int
    end_col_offset: int
    find_preceding_colon: bool=False
    find_preceding_arrow: bool=False
