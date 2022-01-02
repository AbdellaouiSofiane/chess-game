from controllers import AppManager
from views import AppView


GREETING_MESSAGE = """

===============================================================================
    Welcome to our chess tournament application.

    If you have any question, please visit our website.

    Have a nice game !
===============================================================================
"""

if __name__ == '__main__':
    print(GREETING_MESSAGE)
    input('Press ENTER to continu')
    app = AppManager(model=None, view=AppView())
    app.start()
