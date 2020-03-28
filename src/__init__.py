# To start in desktop
#   start http://localhost:5000/
#   poetry run python -m src -m webdebugger
#
# To start the android logcat
#   adb -d logcat *:S python:D

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
# NOTE: Clock.schedule_once(self.remove_load_logo, 2) -> set to 1 when building
# NOTE: import os; os.environ["KIVY_NO_CONSOLELOG"] = '1' use this before build

__version__ = '0.1.0'
