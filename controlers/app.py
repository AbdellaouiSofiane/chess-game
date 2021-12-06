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
            self.view.setup(self)
            self.view.start()


class PlayerManager(BaseManager):

    def create(self):
        first_name = self.view.get_first_name()
        last_name = self.view.get_last_name()
        sexe = self.view.get_sexe()
        rank = self.view.get_rank()
        player = Factory().load(
            {
                'first_name': first_name,
                'last_name': last_name,
                'sexe': sexe,
                'rank': rank
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
        name = self.view.get_name()
        tournament = Factory().load(
            {
                'name': name,
            },
            self.model
        )
        tournament.save()

    def enroll_players(self):
        pass
        # tournaments = [
        #     tournament for tournament
        #     in self.model.all()
        #     if not tournament.ready
        # ]
        # if not tournaments:
        #     print('There is currently no tournament to assign players to.')
        # elif len(tournaments) == 1:
        #     active_tournament = tournaments[0]
        # else:
        #     active_tournament_id = self.view.get_active_tournament(tournaments)
        #     active_tournament = self.model.get(active_tournament_id)

        # not_enrolled_players =

        # while len(active_tournament.players) < active_tournament.nb_rounds * 2:

        # while len(active_tournament.players) < active_tournament.nb_rounds * 2:
        #     print('select a player from the following list')
        #     PlayerManager(model=Player , view=PlayerView()).show_all()
        #     player_id = input()
        #     player = Player.get(int(player_id))
        #     tournament.players.append(player.id)
        #     tournament.save()

    def launch_game(self):
        pass
        # tournaments = [
        #     tournament for tournament
        #     in self.model.all()
        #     if not tournament.is_finished
        # ]
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
