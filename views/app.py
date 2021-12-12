import os
from abc import ABC, abstractmethod



class BaseView(ABC):
    """ Abstract Class for handling common interaction with users."""

    @abstractmethod
    def setup(self, controller):
        """ Required method for child classes.
            Expects a controller class as argument.
            Must define a mapping attribute if the form of:
                {'option_index': {'description': str, 'action': func}, ...}
        """
        pass

    @property
    def menu(self):
        """ Return the menu list to be displayed in the interface"""
        return "\n".join(
            f"\t{index}- {option.get('description')}"
            for index, option in self.mapping.items()
        )

    def start(self):
        """ Display the view's menu and get customer choice."""
        user_choice = input(
            f"Select an action from the menu:\n" +
            f"{self.menu}\n"
            + "=> "
        )
        self.execute(user_choice)

    def execute(self, user_choice):
        """ call the function given a user choice and the view mapping"""
        if user_choice in self.mapping:
            self.mapping.get(user_choice).get('action')()
        else:
            input("Invalid action selected, please try again.\n")
            self.clear()
            self.start()

    def clear(self):
        """ Clear user interface"""
        os.system('cls' if os.name=='nt' else 'clear')

    def display_objects(self, objects_list):
        """ print an enumerated list of objects."""
        print("\n".join(f"\t{i}- {obj}" for i, obj in enumerate(objects_list, 1)))

    def get_selected_object(self, objects_list):
        """ Display an enumerated list of objects and return the object
            selected By the user
        """
        self.display_objects(objects_list)
        user_choice = input('=> ')
        try:
            user_choice = int(user_choice)
            obj = objects_list[user_choice - 1]
        except (ValueError, IndexError):
            input('Invalid choice, please try again:\n')
            return self.get_selected_object(objects_list)
        else:
            return obj


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
