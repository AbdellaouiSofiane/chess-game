from .base import BaseView


class PlayerView(BaseView):

    def setup(self, controller):
        self.mapping = {
            'A': {
                'description': 'Create new player',
                'action': controller.create
            },
            'B': {
                'description': 'Display all registred players',
                'action': controller.show_all
            },
            'C': {
                'description':'Back',
                'action': controller.back
            },
        }

    def get_first_name(self):
        return input('Enter first name:\n =>')

    def get_last_name(self):
        return input('Enter last name:\n')

    def get_sexe(self):
        return input('Enter sexe:\n')

    def get_rank(self):
        return input('Enter rank:\n')

    def display_players(self, players):
        if players:
            print('List of all registred players:')
            self.display_objects(players)
        else:
            print('There is currently no registred player')

        input('\nPress ENTER to continu\n') # avoid clearing interface


class TournamentView(BaseView):

    def setup(self, controller):
        self.mapping = {
            'A': {
                'description':'Create new tournament',
                'action': controller.create
            },
            'B': {
                'description':'Enroll player to tournament',
                'action': controller.enroll_player
            },
            'C': {
                'description':'Launch game',
                'action': controller.launch_game
            },
            'D': {
                'description':'Display all tournament',
                'action': controller.show_all
            },
            'E': {
                'description':'Back',
                'action': controller.back
            },

        }

    def get_player(self, players):
        if players:
            print('Please select a player from the list below:\n')
            obj = self.get_selected_object(players)
            return obj
        else:
            print('No tournament was found:\n')

    def set_score(self, players):
        print('Please select the winner of the match:\n')
        return self.get_selected_object(players)

    def get_active_tournament(self, tournaments):
        if tournaments:
            print('Please select a tournament from the list below:\n')
            obj = self.get_selected_object(tournaments)
            return obj
        else:
            print('No tournament was found:\n')

    def display_tournaments(self, tournaments):
        if tournaments:
            print('List of all registred tournaments:\n')
            self.display_objects(tournaments)
        else:
            print('There is currently no registred tournament')

        input('\nPress ENTER to continu\n') # avoid clearing interface

    def get_name(self):
        return input('Enter a name for the new tournament:\n')


class AppView(BaseView):

    def setup(self, controller):
        self.mapping = {
            'A': {
                'description':'Manage tournaments',
                'action': controller.lunch_tournament_manager
            },
            'B': {
                'description':'Manage players',
                'action': controller.lunch_player_manager
            },
            'C': {
                'description':'Exit program',
                'action': controller.exit
            }
        }
