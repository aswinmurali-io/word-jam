# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
# NOTE: Clock.schedule_once(self.remove_load_logo, 2) -> set to 1 when building
# NOTE: import os; os.environ["KIVY_NO_CONSOLELOG"] = '1' use this before build
# NOTE: add graphics, add levels, optimise linux build, add github actions
# NOTE: add private .kivy folder for the app
# NOTE: optimise the async_lazy_load_level_list(), validate_character()
