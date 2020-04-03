# To start in desktop
#   start http://localhost:5000/
#   poetry run python -m src -m webdebugger
#
# To start the android logcat
#   adb -d logcat *:S python:D
#
# To start the nuika build process
#   conda activate base (poetry installed in anaconda python)
#   poetry run python -m nuitka --follow-imports --msvc=14.0 --include-plugin-directory=nuitka-dependencies.py --include-package=src --windows-disable-console --remove-output --standalone main.py

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
# NOTE: Clock.schedule_once(self.remove_load_logo, 2) -> set to 1 when building
# NOTE: import os; os.environ["KIVY_NO_CONSOLELOG"] = '1' use this before build
# NOTE: add graphics, add levels, optimise linux build, add github actions
# NOTE: add private .kivy folder for the app

__version__ = '0.1.0'
