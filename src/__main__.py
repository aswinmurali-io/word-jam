# !/usr/bin/python
# The main game code

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
# NOTE: Clock.schedule_once(self.remove_load_logo, 2) -> set to 1 when building
# NOTE: import os; os.environ["KIVY_NO_CONSOLELOG"] = '1' use this before build
# NOTE: Strip the apk

import gc
import sys
import kivy
import shutil
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

from src.common import RES, MAX_GRID, DEFAULT_ATLAS, LVL, GRID_HINT, \
    stime, timing, kivy_timing, generate_grid_id

from src.save import GRID, load_level, validate_character, save_level

kivy.require('1.11.1')
Window.set_title("Word Jam")

# Setting up the configuration of the game

Config.set('kivy', 'log_maxfiles', 10)
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'exit_on_escape', True)
Config.set('kivy', 'pause_on_minimize', False)
Config.set('kivy', 'allow_screensaver', False)
Config.set('kivy', 'window_icon', RES + 'win.png')

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

Config.set('graphics', 'width', 580)
Config.set('graphics', 'height', 850)
Config.set('graphics', 'resizable', False)

Config.write()


class WordButton(Button):
    lock = False

    # @kivy_timing -> Slow
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        self.id = generate_grid_id()
        try:
            self.text = str(GRID.popleft())
        except IndexError:
            self.text = 'X'
        self.level_logic()
        self.bind(state=self.on_click)
        self.fade_effect_ptr = Clock.schedule_interval(self.fade_effect, 0.001)
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    # @kivy_timing -> Slow
    def level_logic(self):
        if self.text == '0':
            self.disabled = True
            self.text = ''
        else:
            self.disabled = False
            if self.text.islower():
                self.text = ''

    # @kivy_timing
    def on_click(self, instance, value):
        if self.text == '' and not self.disabled and not WordButton.lock:
            self.text = '?'
            self_pointer.root.ids.status_bar.text = GRID_HINT[int(self.id)][1:-1]
            self.background_normal = ''
            self.background_color = 0, 1, 1, 1
            WordButton.lock = True

    # @kivy_timing -> Slow
    def event_keyboard(self, window, key, *largs):
        if self.text == '?':
            # NOTE: Reload the level data again to check validation This needs
            # to be done because while building the grid all the elements are
            # popped out. Thus the GRID deque was empty.
            load_level(1)
            WordButton.lock = False

            def _(_):
                self.text = ''
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 1, 1, 1

            def _2(_):
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 1, 1, 1

            if validate_character(chr(key), self.id):
                self.text = chr(key).upper()
                save_level(int(self.id), chr(key).upper())
                Clock.schedule_once(_2, 1)
            else:
                self.text = 'X'
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 0, 0, 1
                Clock.schedule_once(_, 1)

    # @kivy_timing -> Slow
    def fade_effect(self, x):
        if self.opacity < 1:
            self.opacity += 0.1
        # Unregister event after use
        elif self.opacity > 1:
            Clock.unschedule(self.fade_effect_ptr)


class MainLayout(Widget):
    pass


class WordJam(App):
    @timing
    def build(self):
        global self_pointer
        self_pointer = self
        return MainLayout()

    @timing
    def on_start(self):
        # Start the grid constructor
        Clock.schedule_once(self.async_grid)
        # Remove the banner logo after use
        Clock.schedule_once(self.remove_load_logo, 1)
        # Start the level timer
        Clock.schedule_interval(self.async_time, 1)
        # Bind android back button to exit
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    @timing
    def on_pause(self):
        gc.collect()
        return True

    @kivy_timing
    def async_time(self, x):
        global stime
        stime = (
            datetime.datetime.strptime(
                stime, '%H:%M:%S'
            ) + datetime.timedelta(seconds=1)
        ).strftime('%H:%M:%S')
        self.root.ids.time.text = '[b]' + stime + '[/b]'

    @kivy_timing
    def async_grid(self, x):
        # Generate the grid using custom button widget in loop
        for i in range(MAX_GRID):
            # Schedule in clock to make it faster (lazy loading)
            Clock.schedule_once(lambda x: self.root.ids.grid.add_widget(
                    WordButton(text=' ')
                )
            )
        return True

    @kivy_timing
    def remove_load_logo(self, x):
        # Delete loading txt after use
        self.root.ids.content.remove_widget(self.root.ids.load)

    @kivy_timing
    def event_keyboard(self, window, key, *largs):
        if key == 27:
            App.get_running_app().stop()


@kivy_timing
def main():
    # For this game, disabling is necessary
    gc.disable()
    # Copy the first level as current level if no save slot is found
    if not os.path.exists(LVL + 'save.csv'):
        shutil.copyfile(LVL + '1.csv', LVL + 'save.csv')
        shutil.copyfile(LVL + '1_hint.csv', LVL + 'save_hint.csv')
    # Load the level
    load_level('save')
    # Fix blurry font because text scalling issue in windows
    if 'win32' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # UI entry point
    WordJam().run()


# Entry point
if __name__ == "__main__":
    main()
