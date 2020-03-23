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
import pickle
import ctypes
import os.path
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.base import EventLoop
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.core.window import Window

from src.common import (
    RES,
    MAX_GRID,
    DEFAULT_ATLAS,
    IS_MOBILE,
    LVL,
    GRID_HINT,
    DEFAULT_STATUS_TEXT,
    COIN_PROGRESS_FILE,
    LEVEL_NUMBER_FILE,
    COIN_PROGRESS,
    stime,
    timing,
    kivy_timing,
    generate_grid_id,
    reset_grid_id,
    self_pointer_to_word_jam_class,
    LEVEL_NUMBER,
)

from src.save import (
    GRID,
    load_level,
    validate_character,
    save_level
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


class WordButton(Button):
    lock: bool = False

    # @kivy_timing -> Slow
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity: float = 0
        self.id: str = generate_grid_id()
        try:
            self.text: str = str(GRID.popleft())
        except IndexError:
            self.text: str = "X"
        self.level_logic()
        self.bind(on_press=self.on_click)
        self.fade_effect_ptr = Clock.schedule_interval(self.fade_effect, 0.001)
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    # @kivy_timing -> Slow
    def level_logic(self) -> None:
        if self.text == "0":
            self.disabled = True
            self.text = ""
        else:
            self.disabled = False
            if self.text.islower():
                self.text = ""

    @kivy_timing
    def on_click(self, *largs) -> None:
        if self.text == "" and not self.disabled and not WordButton.lock:
            self.text = "?"
            WordButton.lock = True
            self.background_normal = ""
            self.background_color = 0, 1, 1, 1
            self_pointer_to_word_jam_class.root.ids.status_bar.text = (
                "Press [b]ESC[/b] to cancel selection"
                if not IS_MOBILE
                else "Press [b]any[/b] letter to cancel selection"
            ) + (
                (", [b]hint[/b]: " + GRID_HINT[int(self.id)][1:-1])
                if GRID_HINT[int(self.id)][1:-1] != ""
                else ""
            )

    # @kivy_timing -> Slow
    def event_keyboard(self, _, key: int, *largs):
        # global LEVEL_NUMBER
        if self.text == "?":
            # NOTE: Reload the level data again to check validation This needs
            # to be done because while building the grid all the elements are
            # popped out. Thus the GRID deque was empty.
            try:
                with open(LEVEL_NUMBER_FILE, 'rb') as pickle_file:
                    load_level(pickle.load(pickle_file))
            except:
                load_level(LEVEL_NUMBER)
            # load_level('save')
            WordButton.lock = False

            # set the grid block to it's orignal form
            def set_grid_block_to_default(*largs):
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 1, 1, 1

            def not_correct_letter(*largs):
                self.text = ""
                set_grid_block_to_default(None)

            def set_status_bar_back_to_default(*largs):
                self_pointer_to_word_jam_class.root.ids.status_bar.text = (
                    DEFAULT_STATUS_TEXT
                )

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
    def fade_effect(self, *largs) -> None:
        if self.opacity < 1:
            self.opacity += 0.1
        # Unregister event after use
        elif self.opacity > 1:
            Clock.unschedule(self.fade_effect_ptr)


class MainLayout(Widget):
    pass


class WordJam(App):
    @timing
    def build(self) -> MainLayout:
        global self_pointer_to_word_jam_class
        self_pointer_to_word_jam_class = self
        return MainLayout()

    @timing
    def on_start(self) -> None:
        # Start the grid constructor
        Clock.schedule_once(self.async_grid)
        # Remove the banner logo after use
        Clock.schedule_once(self.remove_load_logo, 1)
        # Start the level timer
        Clock.schedule_interval(self.async_time, 1)
        # Bind android back button to exit
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    @timing
    def on_pause(self) -> bool:
        gc.collect()
        return True

    # @kivy_timing -> thread
    def async_time(self, *largs) -> None:
        global stime, COIN_PROGRESS
        # setting the time
        stime = (
            datetime.datetime.strptime(stime, "%H:%M:%S")
            + datetime.timedelta(seconds=1)
        ).strftime("%H:%M:%S")
        self.root.ids.time.text = "[b]" + stime + "[/b]"
        # Load the coins from the coin save file
        if os.path.exists(COIN_PROGRESS_FILE):
            with open(COIN_PROGRESS_FILE, "rb") as pickle_file:
                COIN_PROGRESS = pickle.load(pickle_file)
        # Set the coin progress in action bar
        self.root.ids.coins.text = str(COIN_PROGRESS)
        # Load the deque with the next level grid info.

        # NOTE: The LEVEL_NUMBER variable is not updating properly
        # may be because of scope issue therefore the level progress
        # save file is used instead to get the next level number.
        if os.path.exists('flag'):
            # increment_level()
            if os.path.exists(LEVEL_NUMBER_FILE):
                with open(LEVEL_NUMBER_FILE, 'rb') as pickle_file:
                    load_level(pickle.load(pickle_file))
            else:
                load_level(LEVEL_NUMBER)
            # Request redrawing of the grid layout
            Clock.schedule_once(self.async_grid)
            # NOTE: A flag file was created to notify the main script when the
            # next level is required. The main script has no proper scope with
            # the variables like LEVEL_NUMBER, LEVEL_PROGRESS etc. So we used
            # file as a message. Now we delete the file
            os.remove('flag')

    @kivy_timing
    def async_grid(self, *largs) -> bool:
        # Reset the grid id to freshly start the deque GRID for next level
        reset_grid_id()
        # Clean the previous level grids for new once. Must be in clock
        Clock.schedule_once(lambda x: self.root.ids.grid.clear_widgets())
        # Generate the grid using custom button widget in loop
        for i in range(MAX_GRID):
            # Schedule in clock to make it faster (lazy loading)
            Clock.schedule_once(
                lambda x: self.root.ids.grid.add_widget(WordButton(text=" "))
            )
        return True

    @kivy_timing
    def remove_load_logo(self, *largs) -> None:
        # Delete loading txt after use
        self.root.ids.content.remove_widget(self.root.ids.load)

    @kivy_timing
    def event_keyboard(self, _, key: int, *largs) -> None:
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
    # Fix blurry font because text scalling issue in windows
    if "win32" in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # UI entry point
    WordJam().run()


# Entry point
if __name__ == "__main__":
    main()
