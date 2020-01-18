# !/usr/bin/python
# The main game code

# BUG: The pause on minimize feature seems to take too much cpu during idle
# NOTE: The loading of the grid uses kivy clock, not multi-threading (fix it)
# NOTE: Suppress the logging after the game is finished to improve performance
#
# NOTE: Strip the apk
# lib\armeabi-v7a\libcrypto1.1.so
# lib\armeabi-v7a\libsqlite3.so
# res\icon.ico
# res\banner.png
# logs\.*
# tests\.*

import gc
import sys
import kivy
import ctypes
import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.base import EventLoop
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from src.common import RES, MAX_GRID, stime, timing, kivy_timing
from src.save import GRID, load_level

print(GRID)

kivy.require('1.11.1')

# Setting up the configuration of the game

Config.set('kivy', 'log_maxfiles', 10)
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'exit_on_escape', True)
Config.set('kivy', 'pause_on_minimize', False)
Config.set('kivy', 'allow_screensaver', False)
Config.set('kivy', 'window_icon', RES + 'win.png')

Config.set('graphics', 'width', 580)
Config.set('graphics', 'height', 850)

Config.write()


class WordButton(Button):
    @kivy_timing
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opacity = 0
        self.text = str(GRID.popleft())
        self.level_logic()
        self.fade_effect_ptr = Clock.schedule_interval(self.fade_effect, 0.001)

    # @kivy_timing
    def level_logic(self):
        if self.text == '0':
            self.disabled = True
            self.text = ''
        else:
            self.disabled = False

    # @kivy_timing
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
        return MainLayout()

    @timing
    def on_start(self):
        Clock.schedule_once(self.async_grid, 1)
        Clock.schedule_interval(self.async_time, 1)
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
            self.root.ids.grid.add_widget(WordButton(text=' '))

        # Delete loading txt after use
        self.root.ids.content.remove_widget(self.root.ids.load)
        return True

    @kivy_timing
    def event_keyboard(self, window, key, *largs):
        if key == 27:
            sys.exit(0)


@kivy_timing
def main():
    # Load the level
    load_level(1)
    # Fix blurry font because text scalling issue in windows
    if 'win32' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    # UI entry point
    WordJam().run()


# Entry point
if __name__ == "__main__":
    main()
