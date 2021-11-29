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
            return f"{self.player_1}:{self.score_player_1} VS "\
                   f"{self.player_2}:{self.score_player_2}"
        else:
            return f"{self.player_1} VS {self.player_2}"

    @property
    def is_finished(self):
        """ Return a boolean that indicate if the score has been
            settled for this match.
        """
        if self.score_player_1 + self.score_player_2 == 1:
            return True
        return False

    def set_score(self, winner=None):
        """ Set score to 1 for winning player or 0.5 for both
            players if draw.
        """
        if winner == self.player_1:
            self.score_player_1, self.score_player_2 = 1, 0
        elif winner == self.player_2:
            self.score_player_1, self.score_player_2 = 0, 1
        else:
            self.score_player_1, self.score_player_2 = 0.5, 0.5

    def get_score(self, player):
        """ Return the player's score for this match."""
        if player == self.player_1:
            return self.score_player_1
        elif player == self.player_2:
            return self.score_player_2
        return 0


@dataclass
class Round(BaseModel):
    index: int
    matchs: List[Match] = field(default_factory=list)

    def __str__(self):
        return f"Round {self.index}"

    @property
    def is_finished(self):
        """ Return a boolean that indicate if all matchs have been
            settled for this round.
        """
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
        """ Return a boolean that indicate wether all players
            have joined the tournament.
        """
        if len(self.players) == self.nb_rounds * 2:
            return True
        return False

    @property
    def is_finished(self):
        """ Return a boolean that indicate if all rounds has been
            settled for this tournament.
        """
        if (
            len(self.rounds) == self.nb_rounds and
            all(round.is_finished for round in self.rounds)
        ) :
            return True
        return False

    def enroll_player(self, player):
        """ Add a new player to tournament."""
        if (
            player.id not in self.players and
            not self.ready
        ):
            self.players.append(player.id)
            self.save()

    def total_score(self, player):
        """ Return the cumulated score of a given player troughout
            the tournament.
        """
        return sum(
            match.get_score(player)
            for round in self.rounds
            for match in round.matchs
        )

    def generate_next_round(self):
        """ Generate a new round and match players together."""
        players = sorted(
            [Player.get(player) for player in self.players],
            key=lambda x: (self.total_score(x), -x.rank),
            reverse=True
        )

        if self.ready and not self.rounds:
            match_list = [
                Match(players[i], players[i + self.nb_rounds])
                for i in range(self.nb_rounds)
            ]
        elif (self.ready and
              self.rounds[-1].is_finished and
              len(self.rounds) < self.nb_rounds):
            match_list = [
                Match(players[i * 2], players[i * 2 + 1])
                for i in range(self.nb_rounds)
            ]
        else:
            return

        self.rounds.append(
            Round(index=len(self.rounds)+1, matchs=match_list)
        )
        self.save()
