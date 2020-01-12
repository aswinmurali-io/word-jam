#!/usr/bin/python

from __future__ import absolute_import, division, print_function, \
                       unicode_literals
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class MainLayout(BoxLayout):
    def __init__(self):
        super(MainLayout, self).__init__()
        pass


class WordJam(App):
    def build(self):
        self.main_layout = MainLayout(orientation='vertical')
        return self.main_layout


if __name__ == "__main__":
    WordJam().run()
