# !/usr/bin/python
# The main game code

import sys
import kivy
import glob
import shutil
import ctypes
import os.path
import datetime
import cProfile
import threading

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.base import EventLoop
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.core.window import Window

from src.config import *
from src.save import load_level
from src.grid import WordButton, grid_ptr
from src.monitor import timing, kivy_timing

from src.common import (
    SRC,
    LVL,
    RES,
    MAX_GRID,
    IS_MOBILE,
    FONT_COLOR,
    DB_CONNECTION,
    get,
    save,
    reset_grid_id,
    get_level_history,
    save_level_history
)
# COIN_PROGRESS, LEVEL_NUMBER, LEVEL_PROGRESS, LEVEL_TIME
kivy.require("1.11.0")
stime: str = get(level_time=True)  # The level time counter
# To position window for live reload of the project
Window.top = 100
Window.left = 10


class WordJam(App):
    @timing
    def build(self):
        self.title = "Word Jam"
        return Builder.load_file(SRC + "layout.kv")

    @timing
    def on_start(self) -> None:
        # Start the grid constructor if in main layout
        if self.root.current in 'main':
            Clock.schedule_once(self.async_grid)
            # Removing the banner logo after use
            Clock.schedule_once(lambda x: self.root.ids.main.ids.content.remove_widget(self.root.ids.main.ids.load), 1)
        # Build the mobile keyboard
        if IS_MOBILE:
            # Alphabet ASCII range
            for i in range(65, 91):
                # Schedule in clock to make it faster (lazy loading)
                self.root.ids.main.ids.keyboard_layout.add_widget(
                    Button(
                        text=chr(i), bold=True,
                        background_normal=RES + 'grey-button-normal.png',
                        color=FONT_COLOR, on_press=lambda x:
                        threading.Thread(
                            target=self.thread_check_validity_from_mobile_keyboard,
                            args=(grid_ptr, x.text, )
                        ).start()
                    )
                )
            # The cancel alphabet button
            self.root.ids.main.ids.keyboard_layout.add_widget(
                Button(
                    text='⛔', bold=True, font_size=27, on_press=lambda x:
                    threading.Thread(
                        target=self.thread_check_validity_from_mobile_keyboard,
                        args=(grid_ptr, x.text, )
                    ).start()
                )
            )
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
        Logger.info("Lazy Loading: Lazy loading the level list")
        levels: int = len(glob.glob(LVL + '*.csv'))
        records = get_level_history()
        for i in range(1, levels):
            if IS_MOBILE:
                x = Factory.LevelSelectionButton(size_hint_y=4.5, spacing=30)
            else:
                x = Factory.LevelSelectionButton()
            x.level_number = "Level " + str(i)
            try:
                # i - 1 is because we are starting loop i from 1 instead of 0
                x.level_time = records[i - 1][1]
            except IndexError:
                # The current level we need to finish should be in In Progress
                # status not in Not Completed
                if i != get(level_number=True):
                    x.level_time = "Not Completed"
                else:
                    x.level_time = "In Progress, No Records Found"
            root.ids.level_list_layout.add_widget(x)

    # @kivy_timing  # -> thread
    def async_time(self, *_) -> None:
        global stime
        # NOTE: The level_number variable is not updating properly may be
        # because of scope issue therefore the level progress save file is
        # used instead to get the next level number.
        # TODO: Find a better approach later for this logic
        if os.path.exists('flag'):  # -> The next level if condition
            # Load the deque with the next level grid info
            x = get(level_number=True)
            load_level(x)
            # Save the current level time in level history
            save_level_history(x - 1, stime, 0)
            # Reset the level timer for the next level
            stime = '00:00:00'
            save(level_time=stime)
            # Request redrawing of the grid layout
            Clock.schedule_once(self.async_grid)
            # NOTE: A flag file was created to notify the main script when the
            # next level is required. The main script has no proper scope with
            # the variables like level_number, level_progress etc. So we used
            # file as a message. Now we delete the file after use
            os.remove('flag')
        else:
            # updating the time by one second
            stime = (datetime.datetime.strptime(stime, "%H:%M:%S") + datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
            # Save the current level timer
            save(level_time=stime)
        # Detecting if it's Main Layout and applying code logic for it
        if self.root.current in 'main':
            # Update the time in the UI
            self.root.ids.main.ids.time.text = "[b]" + stime + "[/b]"
            # Load the coins from the save file and set the coin progress in UI
            self.root.ids.main.ids.coins.text = str(get(coin_progress=True))

    @kivy_timing
    def thread_check_validity_from_mobile_keyboard(self, ptr, key) -> None:
        def _(*__):
            for widget in ptr:
                widget.event_keyboard(None, key=ord(key))

        Clock.schedule_once(_)

    @kivy_timing
    def async_grid(self, *_) -> bool:
        # Reset the grid id to freshly start the deque GRID for next level
        reset_grid_id()
        # self.root.ids.main.ids.grid.clear_widgets()
        # Clean the previous level grids for new once. Must be in clock
        Clock.schedule_once(lambda x: self.root.ids.main.ids.grid.clear_widgets())
        grid_ptr.clear()
        # Generate the grid using custom button widget in loop
        for i in range(MAX_GRID):
            # Schedule in clock to make it faster (lazy loading)
            Clock.schedule_once(lambda x: self.root.ids.main.ids.grid.add_widget(WordButton(text=" ")))
        for widget in grid_ptr:
            widget.text = ""
        return True

    # Exit handler for android and other mobile devices
    @kivy_timing
    def event_keyboard(self, __, key: int, *_) -> None:
        if key == 27 and IS_MOBILE:
            os._exit(0)


@kivy_timing
def main() -> None:
    # Copy the first level as current level if no save slot is found
    if not os.path.exists(LVL + "save.csv"):
        shutil.copyfile(LVL + "1.csv", LVL + "save.csv")
    # Load the level
    load_level("save")
    # load_level(get(level_number=True))
    # Fix blurry font because text scale issue in windows
    if "win32" in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # UI entry point
    WordJam().run()
    # Close the database after game if closed
    DB_CONNECTION.close()


# Entry point
cProfile.run('main()') if __name__ == "__main__" else None
