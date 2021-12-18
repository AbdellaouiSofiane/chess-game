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
            f"\t[{index}] {option.get('description')}"
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
