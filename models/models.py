from dataclasses import dataclass, field
from typing import List
from .base import BaseModel


@dataclass
class Player(BaseModel):
    first_name: str
    last_name: str
    # birth_day: date
    sexe: str
    rank: int

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@dataclass
class Match(BaseModel):
    player_1: int
    player_2: int
    score_player_1: float = 0
    score_player_2: float = 0

    def __str__(self):
        return "%s: %s VS %s: %s" % (
            Player.get(self.player_1),
            self.score_player_1,
            Player.get(self.player_2),
            self.score_player_2
        )

    @property
    def is_finished(self):
        """ Return a boolean that indicate if the score has been settled
            for this match.
        """
        if self.score_player_1 + self.score_player_2 == 1:
            return True
        return False

    def set_score(self, winner=None):
        """ Set score to 1 for winning player or 0.5 for both players
            if draw.
        """
        if isinstance(winner, Player):
            winner = winner.id
        if winner == self.player_1:
            self.score_player_1, self.score_player_2 = 1, 0
        elif winner == self.player_2:
            self.score_player_1, self.score_player_2 = 0, 1
        else:
            self.score_player_1, self.score_player_2 = 0.5, 0.5

    def get_score(self, player):
        """ Return the player's score for this match."""
        if isinstance(player, Player):
            player = player.id
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
        """ Return a boolean that indicate if all matchs have been settled
            for this round.
        """
        if self.matchs and all(match.is_finished for match in self.matchs):
            return True
        return False

    def get_active_match(self):
        """ Return the first match of the round which is not finished. """
        pending_matchs = [
            match for match in self.matchs if not match.is_finished
        ]
        if pending_matchs:
            return pending_matchs[0]
        return None


@dataclass
class Tournament(BaseModel):
    name: str
    nb_rounds: int = 4
    players: List[int] = field(default_factory=list)
    rounds: List[Round] = field(default_factory=list)

    def __str__(self):
        if not self.is_ready:
            return "%s (%s/%s) players" % (
                self.name,
                len(self.players),
                self.nb_rounds * 2
            )
        elif not self.is_finished:
            return "%s (%s/%s rounds)" % (
                self.name,
                len(self.rounds),
                self.nb_rounds
            )
        else:
            return "%s (finished)" % self.name

    @property
    def is_ready(self):
        """ Return a boolean that indicate wether all players have joined
            the tournament.
        """
        if len(self.players) == self.nb_rounds * 2:
            return True
        return False

    @property
    def is_finished(self):
        """ Return a boolean that indicate if all rounds has been settled for
            this tournament.
        """
        if (
            len(self.rounds) == self.nb_rounds and
            all(round.is_finished for round in self.rounds)
        ):
            return True
        return False

    def get_active_round(self):
        """ Return the active round of a tournament, generate a new round
            if needed.
        """
        if (
            not self.rounds or
            (
                self.rounds[-1].is_finished and
                len(self.rounds) < self.nb_rounds
            )
        ):
            self.generate_next_round()
        if not self.rounds[-1].is_finished:
            return self.rounds[-1]
        return None

    def get_active_match(self):
        """ Return the active match of a tournament"""
        active_round = self.get_active_round()
        if active_round:
            return active_round.get_active_match()
        return None

    def get_sorted_players(self):
        """ return a list of players sorted by total score and by rank. """
        return sorted(
            [player for player in self.players],
            key=lambda x: (self.total_score(x), - Player.get(x).rank),
            reverse=True
        )

    def generate_next_round(self):
        """ Generate a new round and match players together. """
        players = self.get_sorted_players()
        if not self.rounds:
            match_list = [
                Match(players[i], players[i + self.nb_rounds])
                for i in range(self.nb_rounds)
            ]
        else:
            match_list = [
                Match(players[i * 2], players[i * 2 + 1])
                for i in range(self.nb_rounds)
            ]
        self.rounds.append(
            Round(index=len(self.rounds) + 1, matchs=match_list)
        )
        self.save()

    def enroll_player(self, player):
        """ Add a new player to tournament."""
        if isinstance(player, Player):
            player = player.id
        if (
            player not in self.players and
            not self.is_ready
        ):
            self.players.append(player)
            self.save()

    def total_score(self, player):
        """ Return the cumulated score of a given player troughout the
            tournament.
        """
        return sum(
            match.get_score(player)
            for round in self.rounds
            for match in round.matchs
        )

    @classmethod
    def get_ready(cls):
        """ Return a list of all tournament which are not ready. """
        return [
            tournament for tournament in cls.all()
            if tournament.is_ready
        ]

    @classmethod
    def get_unready(cls):
        """ Return a list of all tournament which are not ready. """
        return [
            tournament for tournament in cls.all()
            if not tournament.is_ready
        ]

    @classmethod
    def get_unfinished(cls):
        """ Return a list of all tournament which are not finished. """
        return [
            tournament for tournament in cls.all()
            if not tournament.is_finished and tournament.is_ready
        ]
