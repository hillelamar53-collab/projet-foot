class Player:
    def __init__(self, name, age, position):
        self.name = name
        self.age = age
        self.position = position

    def __repr__(self):
        return f"{self.name} ({self.position}, {self.age} ans)"


class Team:
    def __init__(self, name):
        self.name = name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def __repr__(self):
        return f"Equipe {self.name} - {len(self.players)} joueurs"

