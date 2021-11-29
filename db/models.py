from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, ClassVar
from .base import BaseModel


@dataclass(order=True)
class Player(BaseModel):
    first_name: str
    last_name: str
    #birth_day: date
    sexe: str
    rank: int

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@dataclass
class Match(BaseModel):
    player_1: Player
    player_2: Player
    score_player_1: float = 0
    score_player_2: float = 0

    def __str__(self):
        if self.is_finished:
            return f"{self.player_1}:{self.score_player_1} VS {self.player_2}:{self.score_player_2}"
        else:
            return f"{self.player_1} VS {self.player_2}"

    @property
    def is_finished(self):
        if self.score_player_1 + self.score_player_2 == 1:
            return True
        return False

    def set_score(self, winner=None):
        if winner == self.player_1:
            self.score_player_1 = 1
            self.score_player_2 = 0
        elif winner == self.player_2:
            self.score_player_1 = 0
            self.score_player_2 = 1
        else:
            self.score_player_1 = 0.5
            self.score_player_2 = 0.5

    def get_score(self, player):
        if player == self.player_1:
            return self.score_player_1
        elif player == self.player_2:
            return self.score_player_2
        else:
            raise Exception(f"{player} didn't participate in this match")


@dataclass
class Round(BaseModel):
    index: int
    matchs: List[Match] = field(default_factory=list)

    def __str__(self):
        return f"Round {self.index}"

    @property
    def is_finished(self):
        if self.matchs and all(match.is_finished for match in self.matchs) :
            return True
        return False


@dataclass
class Tournament(BaseModel):
    name: str
    nb_rounds: int = 4
    players: List[int] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)

    def __str__(self):
        return f"{self.name}"

    @property
    def ready(self):
        """ A boolean that indicate wether enough players have joined the
            tournament for it to start.
        """
        if len(self.players) == self.nb_rounds * 2:
            return True
        return False

    @property
    def is_finished(self):
        if (
            len(self.rounds) == self.nb_rounds and
            all(round.is_finished for round in self.rounds)
        ) :
            return True
        return False

    def enroll_player(self, player):
        if (
            player.id not in self.players and
            not self.ready
        ):
            self.players.append(player.id)
            self.save()

    def total_score(self, player):
        score = 0
        for round in self.rounds:
            for match in round.matchs:
                if player in [match.player_1, match.player_2]:
                    score += match.get_score(player)
        return score

    def generate_next_round(self):
        if self.ready and not self.is_finished:
            players = [Player.get(player) for player in self.players]

            if not self.rounds:
                players.sort(key=lambda x: x.rank, reverse=True)
                round = Round(index=1)
                for i in range(self.nb_rounds):
                    round.matchs.append(Match(players[i], players[i+self.nb_rounds]))
                self.rounds.append(round)
                self.save()
            elif self.rounds[-1].is_finished and len(self.rounds) < self.nb_rounds:
                players.sort(key=lambda x: (self.total_score(x), x.rank), reverse=True)
                round = Round(index=len(self.rounds) + 1)
                for i in range(self.nb_rounds - round.index):
                    round.matchs.append(Match(players[i], players[i+1]))
                else:
                    if round.index == self.nb_rounds:
                        round.matchs.append(Match(players[0], players[1]))
                self.rounds.append(round)
                self.save()
