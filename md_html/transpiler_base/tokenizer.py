import dataclasses


@dataclasses.dataclass
class Token:
    type: str
    start: int
    stop: int
    value: str

    def __eq__(self, other: str) -> bool:
        return self.type == other
