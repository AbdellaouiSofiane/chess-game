from utils import index_generator
from .base import BaseView


class PlayerView(BaseView):

    def setup(self, controller):
        generator = index_generator()
        self.mapping = {
            generator.__next__(): {
                'description': 'Create new player',
                'action': controller.create
            }
        }
        if controller.model.all():
            self.mapping.update(
                {
                    generator.__next__(): {
                        'description': 'Display all registred players',
                        'action': controller.show_all
                    },
                    generator.__next__(): {
                        'description': 'Update players ranking',
                        'action': controller.update_rank
                    }
                }
            )
        self.mapping.update(
            {
                generator.__next__(): {
                    'description':'Back',
                    'action': controller.back
                }
            }
        )

    def get_first_name(self):
        return input('Enter first name:\n =>')

    def get_last_name(self):
        return input('Enter last name:\n')

    def get_sexe(self):
        return input('Enter sexe:\n')

    def get_rank(self):
        return input('Enter rank:\n')

    def display_players(self, players):
        print('List of all registred players:')
        self.display_objects(players)
        input('\nPress ENTER to continu\n') # avoid clearing interface

    def update_rank(self, players):
        print('Select a player from the list below:\n')
        obj = self.get_selected_object(players)
        rank = input('Enter a new rank for the player:\n=>')
        return obj, rank


class TournamentView(BaseView):

    def setup(self, controller):
        generator = index_generator()
        self.mapping = {
            generator.__next__(): {
                'description':'Create new tournament',
                'action': controller.create
            }
        }
        if controller.model.get_unready():
            self.mapping.update(
                {
                    generator.__next__(): {
                        'description':'Enroll player to tournament',
                        'action': controller.enroll_player
                    }
                }
            )
        if controller.model.get_unfinished():
            self.mapping.update(
                {
                    generator.__next__(): {
                        'description':'Enter results',
                        'action': controller.enter_results
                    }
                }
            )
        if controller.model.all():
            self.mapping.update(
                {
                    generator.__next__(): {
                        'description':'Display all tournament',
                        'action': controller.show_all
                    }
                }
            )
        self.mapping.update(
            {
                generator.__next__(): {
                    'description':'Back',
                    'action': controller.back
                },

            }
        )

    def get_player(self, players, tournament):
        print(f'Please select a player to enroll in {tournament.name}:\n')
        obj = self.get_selected_object(players)
        return obj

    def set_score(self, players, tournament):
        print(f'{tournament}')
        print(f'Please select the winner of the match {tournament.get_active_match()}:\n')
        return self.get_selected_object(players)

    def get_active_tournament(self, tournaments):
        print('Please select a tournament from the list below:\n')
        obj = self.get_selected_object(tournaments)
        return obj

    def display_tournaments(self, tournaments):
        print('List of all registred tournaments:\n')
        self.display_objects(tournaments)
        input('\nPress ENTER to continu\n') # avoid clearing interface

    def get_name(self):
        return input('Enter a name for the new tournament:\n')


class AppView(BaseView):

    def setup(self, controller):
        generator = index_generator()
        self.mapping = {
            generator.__next__(): {
                'description':'Manage tournaments',
                'action': controller.lunch_tournament_manager
            },
            generator.__next__(): {
                'description':'Manage players',
                'action': controller.lunch_player_manager
            },
            generator.__next__(): {
                'description':'Exit program',
                'action': controller.exit
            }
        }
