
from kivy.app import App
from kivy.factory import Factory

class TestApp(App):
    def build(self):
        return Factory.Button(text="Hello")

def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}

# first run
reset()
TestApp().run()
reset()
TestApp().run()
reset()
TestApp().run()