from sys import exit
from dataclass_factory import Factory
from models import Player, Tournament
from views import AppView, PlayerView, TournamentView
from .base import BaseManager


class PlayerManager(BaseManager):
    """ Controller class for Player model"""

    def create(self):
        """ Create and save a new player. """
        player = Factory().load(
            {
                'first_name': self.view.get_first_name(),
                'last_name': self.view.get_last_name(),
                'sexe': self.view.get_sexe(),
                'rank': self.view.get_rank()
            },
            self.model
        )
        player.save()

    def show_all(self):
        """ Display all registred players in the interface. """
        self.view.display_players(self.model.all())

    def back(self):
        """ Go back to App manager. """
        AppManager(view=AppView()).start()


class TournamentManager(BaseManager):

    def create(self):
        """ Create and save a new tournament """
        tournament = Factory().load(
            {
                'name': self.view.get_name()
            },
            self.model
        )
        tournament.save()

    def not_enrolled_players(self):
        """ Return a list of registred players not yet enrolled in the
            active tournament.
        """
        return [
            player for player in Player.all()
            if player.id not in self.active_tournament.players
        ]

    def set_active_tournament(self, tournaments):
        """ set active_tournament class attribute to the tournament 
            given as args, if multiple tournament given then ask user to
            choose one.
        """
        if len(tournaments) == 1:
            self.active_tournament = tournaments[0]
        elif len(tournaments) > 1:
            self.active_tournament = self.view.get_active_tournament(tournaments)
        else:
            self.active_tournament = None

    def enroll_player(self):
        """ Enroll a new player to the active tournament. """
        self.set_active_tournament(self.model.get_unready())
        players = self.not_enrolled_players()
        if players:
            player = self.view.get_player(players, self.active_tournament)
            self.active_tournament.enroll_player(player)

    def enter_results(self):
        self.set_active_tournament(self.model.get_unfinished())
        active_match = self.active_tournament.get_active_match()
        if active_match:
            self.set_score(active_match, self.active_tournament)
            self.active_tournament.save()

    def set_score(self, match, tournament):
        players = [
            Player.get(match.player_1),
            Player.get(match.player_2),
            'draw'
        ]
        winner = self.view.set_score(players, tournament)
        if winner == 'draw':
            match.set_score()
        else:
            match.set_score(winner)

    def show_all(self):
        tournaments = self.model.all()
        self.view.display_tournaments(tournaments)

    def back(self):
        AppManager(model=None, view=AppView()).start()


class AppManager(BaseManager):

    def exit(self):
        exit()

    def lunch_player_manager(self):
        PlayerManager(model=Player , view=PlayerView()).start()

    def lunch_tournament_manager(self):
        TournamentManager(model=Tournament, view=TournamentView()).start()
