from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    position: str
    age: int

    @staticmethod
    def from_row(row: tuple) -> "Player":
        # row = (id, name, position, age)
        return Player(id=row[0], name=row[1], position=row[2], age=row[3])