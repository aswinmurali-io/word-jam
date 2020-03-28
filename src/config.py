# Setting up the configuration of the game

from kivy.config import Config
from src.common import RES

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
