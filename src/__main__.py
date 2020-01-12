#!/usr/bin/python
import kivy

from kivy.app import App
from kivy.config import Config
from kivy.uix.widget import Widget

from src.common import LOG, RES

kivy.require('1.11.1')

# Setting up the configuration of the game
Config.set('kivy', 'log_dir', LOG)
Config.set('kivy', 'allow_screensaver', False)
Config.set('kivy', 'exit_on_escape', True)
Config.set('kivy', 'pause_on_minimize', True)
Config.set('kivy', 'window_icon', RES + 'win.png')

Config.write()


class MainLayout(Widget):
    pass


class WordJam(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    WordJam().run()
