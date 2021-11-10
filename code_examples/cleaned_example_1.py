from dataclasses import dataclass
from typing import NamedTuple


class MyClass:

    def my_method(self, e, f):
        pass


def my_function(i, j):
    pass

class MyTuple(NamedTuple):
    m: 15
    n: 16

@dataclass
class MyDataClass:
    o: 17
    p: 18
