# !/usr/bin/python
# The main game code
# adb -d logcat *:S python:D

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
# NOTE: Clock.schedule_once(self.remove_load_logo, 2) -> set to 1 when building
# NOTE: import os; os.environ["KIVY_NO_CONSOLELOG"] = '1' use this before build

import sys
import kivy
import glob
import shutil
import ctypes
import os.path
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.config import Config
from kivy.base import EventLoop
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.core.window import Window

from src.monitor import timing, kivy_timing

from src.common import (
    RES,
    SRC,
    LVL,
    MAX_GRID,
    IS_MOBILE,
    GRID_HINT,
    DEFAULT_ATLAS,
    DB_CONNECTION,
    DEFAULT_STATUS_TEXT,
    get,
    save,
    reset_grid_id,
    generate_grid_id,
    get_level_history,
    save_level_history
)

from src.save import (
    GRID,
    load_level,
    save_level,
    validate_character
)

kivy.require("1.11.1")
Window.set_title("Word Jam")

# Setting up the configuration of the game

Config.set("kivy", "log_maxfiles", 10)
Config.set("kivy", "log_level", "info")
Config.set("kivy", "exit_on_escape", False)
Config.set("kivy", "pause_on_minimize", False)
Config.set("kivy", "allow_screensaver", False)
Config.set("kivy", "window_icon", RES + "win.png")

Config.set("input", "mouse", "mouse,multitouch_on_demand")

Config.set("graphics", "width", 580)
Config.set("graphics", "height", 850)
Config.set("graphics", "resizable", False)

Config.write()

stime: str = get(LEVEL_TIME=True)  # The level time counter
self_pointer_to_word_jam_class = None  # The application self pointer


# The custom widget which will use to construct grids for the
# cross word levels. This is actually a button widget with some
# custom logic to fit the needs of this game
class WordButton(Button):
    # To prevent mulitple selection which use a static
    # variable to lock the grid
    lock: bool = False

    # @kivy_timing -> Slow
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity: float = 0.0
        self.id: str = generate_grid_id()
        self.disabled: bool = True
        self.text: str = str(GRID.popleft()) if len(GRID) >= 0 else "X"
        self.level_logic()
        self.bind(on_press=self.on_click)
        self.fade_effect_ptr = Clock.schedule_interval(self.fade_effect, 0.001)
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    # @kivy_timing -> Slow
    def level_logic(self) -> None:
        if self.text == "0":
            self.text = ""
        else:
            self.disabled = False
            if self.text.islower():
                self.text = ""

    @kivy_timing
    def on_click(self, *_) -> None:
        if self.text == "" and not self.disabled and not WordButton.lock:
            self.text = "?"
            WordButton.lock = True
            self.background_normal = ""
            self.background_color = 0, 1, 1, 1

            # TODO: ugly code line below. Make it neat later
            self_pointer_to_word_jam_class.root.ids.main.ids.status_bar.text = (
                "Press [b]ESC[/b] to cancel selection"
                if not IS_MOBILE
                else "Press [b]any[/b] letter to cancel selection"
            ) + (
                (", [b]hint[/b]: " + GRID_HINT[int(self.id)][1:-1])
                if GRID_HINT[int(self.id)][1:-1] != ""
                else ""
            )

    # @kivy_timing -> Slow
    def event_keyboard(self, __, key: int, *_):
        if self.text == "?":
            # NOTE: Reload the level data again to check validation This needs
            # to be done because while building the grid all the elements are
            # popped out. Thus the GRID deque was empty.
            load_level(get(LEVEL_NUMBER=True))
            WordButton.lock = False

            # set the grid block to it's original form
            def set_grid_block_to_default(*_):
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 1, 1, 1

            def not_correct_letter(*_):
                self.text = ""
                set_grid_block_to_default(None)

            def set_status_bar_back_to_default(*_):
                self_pointer_to_word_jam_class.root.ids.main.ids.status_bar.text = DEFAULT_STATUS_TEXT

            # Android Back button or Esc key
            if key == 27:
                Clock.schedule_once(not_correct_letter, 1)

            if validate_character(chr(key), self.id):
                self.text = chr(key).upper()
                save_level(int(self.id), chr(key).upper())
                Clock.schedule_once(set_grid_block_to_default, 1)
            else:
                self.text = "X"
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 0, 0, 1
                Clock.schedule_once(not_correct_letter, 1)

            Clock.schedule_once(set_status_bar_back_to_default, 5)

    # @kivy_timing -> Slow
    def fade_effect(self, *_) -> None:
        if self.opacity < 1:
            self.opacity += 0.1
        # Unregister event after use
        elif self.opacity > 1:
            Clock.unschedule(self.fade_effect_ptr)


class WordJam(App):
    @timing
    def build(self):
        # This is a global class pointer approach where the self of a class is
        # stored in a different global variable so that the class can be
        # accessed from everywhere within the file. Remember as this is a very
        # dynamic approach and therefore should be handled carefully
        global self_pointer_to_word_jam_class
        self_pointer_to_word_jam_class = self
        return Builder.load_file(SRC + "layout.kv")

    @timing
    def on_start(self) -> None:
        # Start the grid constructor if in main layout
        if self.root.current in 'main':
            Clock.schedule_once(self.async_grid)
            # Removing the banner logo after use
            Clock.schedule_once(lambda x: self.root.ids.main.ids.content.remove_widget(self.root.ids.main.ids.load), 1)
        # Start the timer event function
        Clock.schedule_interval(self.async_time, 1)
        # Bind android back button to exit
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    @timing
    def on_pause(self) -> bool:
        return True

    @staticmethod
    @timing
    def async_lazy_load_level_list(root) -> None:
        # First we removed the old widgets from the layout to refresh it with
        # with new widgets as the level list gets updated every time when the
        # the player wins a level
        root.ids.level_list_layout.clear_widgets()
        Logger.info("Lazy Loading: Lazy loading the level list for level list layout")
        levels: int = len(glob.glob(LVL + '*.csv'))
        records = get_level_history()
        for i in range(1, levels):
            x = Factory.LevelSelectionButton()
            x.level_number = "Level " + str(i)
            try:
                # i - 1 is because we are starting loop i from 1 instead of 0
                x.level_time = records[i - 1][1]
            except IndexError:
                # The current level we need to finish should be in In Progress
                # status not in Not Completed
                if i != get(LEVEL_NUMBER=True):
                    x.level_time = "Not Completed"
                else:
                    x.level_time = "In Progress, No Records Found"
            root.ids.level_list_layout.add_widget(x)

    # @kivy_timing -> thread
    def async_time(self, *_) -> None:
        global stime
        # NOTE: The LEVEL_NUMBER variable is not updating properly
        # may be because of scope issue therefore the level progress
        # save file is used instead to get the next level number.
        # TODO: Find a better approach later for this logic
        if os.path.exists('flag'):  # -> The next level if condition
            # Load the deque with the next level grid info
            x = get(LEVEL_NUMBER=True)
            load_level(x)
            # Save the current level time in level history
            save_level_history(x - 1, stime, 0)
            # Reset the level timer for the next level
            stime = '00:00:00'
            save(LEVEL_TIME=stime)
            # Request redrawing of the grid layout
            Clock.schedule_once(self.async_grid)
            # NOTE: A flag file was created to notify the main script when the
            # next level is required. The main script has no proper scope with
            # the variables like LEVEL_NUMBER, LEVEL_PROGRESS etc. So we used
            # file as a message. Now we delete the file after use
            os.remove('flag')
        else:
            # updating the time by one second
            stime = (datetime.datetime.strptime(stime, "%H:%M:%S") + datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
            # Save the current level timer
            save(LEVEL_TIME=stime)
        # Detecting if it's Main Layout and applying code logic for it
        if self.root.current in 'main':
            # Update the time in the UI
            self.root.ids.main.ids.time.text = "[b]{stime}[/b]".format(**globals())
            # Load the coins from the save file and set the coin progress in UI
            self.root.ids.main.ids.coins.text = str(get(COIN_PROGRESS=True))

    @kivy_timing
    def async_grid(self, *_) -> bool:
        # Reset the grid id to freshly start the deque GRID for next level
        reset_grid_id()
        # if self.root.current in 'main':
        # Clean the previous level grids for new once. Must be in clock
        Clock.schedule_once(lambda x: self.root.ids.main.ids.grid.clear_widgets())
        # Generate the grid using custom button widget in loop
        for i in range(MAX_GRID):
            # Schedule in clock to make it faster (lazy loading)
            Clock.schedule_once(lambda x: self.root.ids.main.ids.grid.add_widget(WordButton(text=" ")))
        return True

    # Exit handler for android and other mobile devices
    @kivy_timing
    def event_keyboard(self, __, key: int, *_) -> None:
        if key == 27 and IS_MOBILE and not WordButton.lock:
            App.get_running_app().stop()


@kivy_timing
def main() -> None:
    # Copy the first level as current level if no save slot is found
    if not os.path.exists(LVL + "save.csv"):
        shutil.copyfile(LVL + "1.csv", LVL + "save.csv")
    # Load the level
    load_level("save")
    # Fix blurry font because text scale issue in windows
    if "win32" in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # UI entry point
    WordJam().run()
    # Close the database after game if closed
    DB_CONNECTION.close()


# Entry point
main() if __name__ == "__main__" else None
