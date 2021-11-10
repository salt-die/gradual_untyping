class MyClass:
    a: list[
        list[str]
    ]
    b: dict[
        tuple, dict[str, int]
    ]

    def spam(
        self,
        a,
        b: list[
            list[str]
        ],
        c,
    ) -> None:
        return 42
