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

    def not_enrolled_players(self, tournament):
        """ Return a list of registred players not yet enrolled in the
            tournament given as arg.
        """
        return [
            player for player in Player.all()
            if player.id not in tournament.players
        ]

    def get_active_tournament(self, default=True):
        if default:
            tournaments = self.model.get_unready()
        else:
            tournaments = self.model.get_unfinished()
        if tournaments and len(tournaments) == 1:
            return tournaments[0]
        elif tournaments and len(tournaments) > 1:
            return self.view.get_active_tournament(tournaments)
        return None

    def enroll_player(self):
        tournament = self.get_active_tournament()
        if tournament:
            players = self.not_enrolled_players(tournament)
            if players:
                player = self.view.get_player(players)
                tournament.enroll_player(player)
            else:
                input("There's no player to enroll.")
        else:
            input("There's no open tournament.\n")

    def launch_game(self):
        tournament = self.get_active_tournament(default=False)
        if tournament:
            active_match = tournament.get_active_match()
            if active_match:
                self.set_score(active_match)
                tournament.save()
        else:
            input("There's no open tournament.\n")

    def set_score(self, match):
        players = [
            Player.get(match.player_1),
            Player.get(match.player_2),
            'draw'
        ]
        winner = self.view.set_score(players)
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
