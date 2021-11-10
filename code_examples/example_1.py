from dataclasses import dataclass
from typing import NamedTuple

a: 1
b: 2

class MyClass:
    c: 3
    d: 4

    def my_method(self, e: 5, f: 6) -> 7:
        g: 8
        h: 9


def my_function(i: 10, j: 11) -> 12:
    k: 13
    l: 14

class MyTuple(NamedTuple):
    m: 15
    n: 16

@dataclass
class MyDataClass:
    o: 17
    p: 18
