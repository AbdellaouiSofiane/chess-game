import sys
from abc import ABC

from dataclass_factory import Factory

from models import Player, Tournament
from views.app import AppView, PlayerView, TournamentView



class BaseManager(ABC):

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def start(self):
        while True:
            self.view.clear()
            self.view.setup(self)
            self.view.start()


class PlayerManager(BaseManager):

    def create(self):
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
        players = self.model.all()
        self.view.display_players(players)

    def back(self):
        AppManager(model=None, view=AppView()).start()


class TournamentManager(BaseManager):

    def create(self):
        tournament = Factory().load(
            {'name': self.view.get_name()}, self.model
        )
        tournament.save()

    def not_enrolled_players(self, tournament):
        return [
            player for player in Player.all()
            if player.id not in tournament.players
        ]

    def get_active_tournament(self):
        tournaments = self.model.get_unready()
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
        tournaments = self.model.get_unfinished()
        tournament = self.view.get_active_tournament(tournaments)

        # if not tournaments:
        #     print('There is currently no tournament to launch.')
        # elif len(tournaments) == 1:
        #     active_tournament = tournaments[0]
        # else:
        #     active_tournament_id = self.view.get_active_tournament(tournaments)
        #     active_tournament = self.model.get(active_tournament_id)


    def show_all(self):
        tournaments = self.model.all()
        self.view.display_tournaments(tournaments)

    def back(self):
        AppManager(model=None, view=AppView()).start()


class AppManager(BaseManager):

    def exit(self):
        sys.exit()

    def lunch_player_manager(self):
        PlayerManager(model=Player , view=PlayerView()).start()

    def lunch_tournament_manager(self):
        TournamentManager(model=Tournament, view=TournamentView()).start()
