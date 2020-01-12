# !/usr/bin/python
# The main game code

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance

import gc
import sys
import kivy
import ctypes

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.base import EventLoop
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from src.common import LOG, RES, MAX_GRID

kivy.require('1.11.1')

# Setting up the configuration of the game
Config.set('kivy', 'log_dir', LOG)
Config.set('kivy', 'exit_on_escape', True)
Config.set('kivy', 'pause_on_minimize', False)
Config.set('kivy', 'allow_screensaver', False)
Config.set('kivy', 'window_icon', RES + 'win.png')

Config.write()


class WordButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MainLayout(Widget):
    pass


class WordJam(App):
    def build(self):
        return MainLayout()

    def on_start(self):
        Clock.schedule_once(self.async_grid, 1)
        EventLoop.window.bind(on_keyboard=self.event_keyboard)

    def on_pause(self):
        gc.collect()
        return True

    def async_grid(self, x):
        for i in range(MAX_GRID):
            self.root.ids.grid.add_widget(WordButton(text='X'))
        return True

    def event_keyboard(self, window, key, *largs):
        if key == 27:
            sys.exit(0)


if __name__ == "__main__":
    # Fix blurry font because text scalling issue in windows
    if 'win32' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # Entry point
    WordJam().run()
