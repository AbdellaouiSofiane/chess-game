from abc import ABC, abstractmethod


class BaseView(ABC):

    @abstractmethod
    def setup(self, controller):
        pass

    @property
    def menu_list(self):
        return "\n".join(
            f"\t{index}- {option.get('description')}"
            for index, option in self.mapping.items()
        )

    def start(self, retry=False):
        if not retry:
            output_message = (
                f"Select an action from the menu:\n {self.menu_list}\n"
            )
        else:
            output_message = (
                f"Invalid action selected, please try again:\n {self.menu_list}\n"
            )

        user_choice = input(output_message + "=> ")

        if user_choice not in self.mapping:
            self.prompt_for_option(retry=True)
        self.mapping.get(user_choice).get('action')()


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
            for player in players:
                print(f"\t{player.id}- {player}")
        else:
            print('There is currently no registred player')


class TournamentView(BaseView):

    def setup(self, controller):
        self.mapping = {
            'A': {
                'description':'Create new tournament',
                'action': controller.create
            },
            'B': {
                'description':'Enroll players to tournament',
                'action': controller.enroll_players
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

    def get_active_tournament(self, tournaments):
        print('Please select the tournament you want to enroll players to:\n')
        for tournament in tournaments:
                print(f"\t{tournament.id}- {tournament.name}")

        return input('=>')

    def display_tournaments(self, tournaments):
        if len(tournaments)  == 0:
            print('There is currently no registred tournament')
        else:
            print('List of all registred tournaments:\n')
            for tournament in tournaments:
                print(f"\t{tournament.id}- {tournament.name}")

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
