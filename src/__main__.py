# !/usr/bin/python
# The main game code

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
# NOTE: Clock.schedule_once(self.remove_load_logo, 2) -> set to 1 when building
# NOTE: import os; os.environ["KIVY_NO_CONSOLELOG"] = '1' use this before build

import gc
import sys
import kivy
import shutil
import ctypes
import os.path
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.config import Config
from kivy.base import EventLoop
from kivy.uix.button import Button
from kivy.core.window import Window

from src.monitor import timing, kivy_timing

from src.common import (
    RES,
    LVL,
    MAX_GRID,
    IS_MOBILE,
    GRID_HINT,
    DEFAULT_ATLAS,
    DB_CONNECTION,
    DEFAULT_STATUS_TEXT,
    get,
    reset_grid_id,
    generate_grid_id
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
Config.set("kivy", "log_level", "debug")
Config.set("kivy", "exit_on_escape", False)
Config.set("kivy", "pause_on_minimize", False)
Config.set("kivy", "allow_screensaver", False)
Config.set("kivy", "window_icon", RES + "win.png")

Config.set("input", "mouse", "mouse,multitouch_on_demand")

Config.set("graphics", "width", 580)
Config.set("graphics", "height", 850)
Config.set("graphics", "resizable", False)

Config.write()

stime: str = "00:00:00"  # The level time counter
self_pointer_to_word_jam_class: App = None


class WordButton(Button):
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

        return Builder.load_file("layout.kv")

    @timing
    def on_start(self) -> None:
        # Start the grid constructor if in main layout
        if self.root.current in 'main':
            Clock.schedule_once(self.async_grid)
        # Start the timer event function
        Clock.schedule_interval(self.async_time, 1)
        # Bind android back button to exit
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    @timing
    def on_pause(self) -> bool:
        gc.collect()
        return True

    # @kivy_timing -> thread
    def async_time(self, *_) -> None:
        global stime
        # updating the time by one second
        stime = (datetime.datetime.strptime(stime, "%H:%M:%S") + datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
        # Detecting if it's Main Layout and applying code logic for it
        if self.root.current in 'main':
            # Removing the banner logo after use
            Clock.schedule_once(lambda x: self.root.ids.main.ids.content.remove_widget(self.root.ids.main.ids.load), 1)
            # Update the time in the UI
            self.root.ids.main.ids.time.text = "[b]" + stime + "[/b]"
            # Load the coins from the save file and set the coin progress in UI
            self.root.ids.main.ids.coins.text = str(get(COIN_PROGRESS=True))

        # NOTE: The LEVEL_NUMBER variable is not updating properly
        # may be because of scope issue therefore the level progress
        # save file is used instead to get the next level number.
        # TODO: Find a better approach later for this logic
        if os.path.exists('flag'):
            # Load the deque with the next level grid info.
            load_level(get(LEVEL_NUMBER=True))
            # Request redrawing of the grid layout
            Clock.schedule_once(self.async_grid)
            # NOTE: A flag file was created to notify the main script when the
            # next level is required. The main script has no proper scope with
            # the variables like LEVEL_NUMBER, LEVEL_PROGRESS etc. So we used
            # file as a message. Now we delete the file after use
            os.remove('flag')

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
    # For this game, disabling is necessary
    gc.disable()
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
