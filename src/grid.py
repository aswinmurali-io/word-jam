from kivy.clock import Clock
from kivy.base import EventLoop
from kivy.uix.button import Button

from src.monitor import kivy_timing

from src.common import (
    GRID_HINT,
    DEFAULT_ATLAS,
    get,
    generate_grid_id
)

from src.save import (
    GRID,
    load_level,
    save_level,
    validate_character
)

# All the grid custom widget ids will be store here. This is because the ids
# are not stored in kivy layout ids because there were dynamically updated so
# we manually store the id reference of all the word button object
grid_ptr: list = []


# The custom widget which will use to construct grids for the cross word
# levels. This is actually a button widget with some custom logic for the game
class WordButton(Button):
    # To prevent mulitple selection we use a static variable to lock the grid
    lock: bool = False

    # @kivy_timing -> Slow
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        grid_ptr.append(self)
        self.opacity: float = 0.0
        self.id: str = generate_grid_id()
        self.next_auto_selection_id = self.id
        self.disabled: bool = True
        self.text: str = str(GRID.popleft()) if len(GRID) >= 0 else 'X'
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
        if self.text == "" and not self.disabled and WordButton.lock:
            self.text = "?"
            # remove previous selection
            for widget in grid_ptr:
                if widget.text == "?" and widget != self:
                    widget.background_normal = DEFAULT_ATLAS
                    widget.background_color = 1, 1, 1, 1
                    widget.text = ""
            self.background_normal = ""
            self.background_color = 0, 1, 1, 1

    # @kivy_timing ->
    def event_keyboard(self, __, key: int, *_):
        if self.text == "?":
            # NOTE: Reload the level data again to check validation This needs
            # to be done because while building the grid all the elements are
            # popped out. Thus the GRID deque was empty.
            load_level(get(level_number=True))
            WordButton.lock = False

            # set the grid block to it's original form
            def set_grid_block_to_default(*_):
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 1, 1, 1
                print(GRID_HINT)
                print("selection=", GRID_HINT[int(self.id)].split())
                try:
                    selection = GRID_HINT[int(self.id)].split()[1]
                except IndexError:
                    selection = '0'
                if selection == 'd':
                    self.next_auto_selection_id = str(int(self.id) + 14)
                if selection == 'dd':
                    self.next_auto_selection_id = str(int(self.id) + 28)

                elif selection == 'u':
                    self.next_auto_selection_id = str(int(self.id) - 14)
                if selection == 'uu':
                    self.next_auto_selection_id = str(int(self.id) - 28)

                elif selection == 'l':
                    self.next_auto_selection_id = str(int(self.id) - 1)
                elif selection == 'll':
                    self.next_auto_selection_id = str(int(self.id) - 2)

                elif selection == 'r':
                    self.next_auto_selection_id = str(int(self.id) + 1)
                elif selection == 'rr':
                    self.next_auto_selection_id = str(int(self.id) + 2)

                elif selection == 'dr':
                    x = str(int(self.id) + 14)
                    self.next_auto_selection_id = str(int(x) + 1)
                elif selection == 'ur':
                    x = str(int(self.id) - 14)
                    self.next_auto_selection_id = str(int(x) + 1)

                elif selection == 'dl':
                    x = str(int(self.id) + 14)
                    self.next_auto_selection_id = str(int(x) - 1)
                elif selection == 'ul':
                    x = str(int(self.id) - 14)
                    self.next_auto_selection_id = str(int(x) - 1)

                elif selection == '0':
                    self.next_auto_selection_id = '0'
                for widget in grid_ptr:
                    try:
                        if widget.id == self.next_auto_selection_id != self.id and not widget.text.upper():
                            widget.background_normal = ""
                            widget.background_color = 0, 1, 1, 1
                            widget.text = '?'
                    except AttributeError:
                        pass
                WordButton.lock = True

            def not_correct_letter(*_):
                self.text = ""
                set_grid_block_to_default(None)

            # Android Back button or Esc key
            if key == 27:
                Clock.schedule_once(not_correct_letter, 1)

            # The key mush be the ascii value of the lowercase character as
            # the save file contains the lowercase chararcter to validate with
            if validate_character(chr(key).lower(), self.id):
                self.text = chr(key).upper()
                save_level(int(self.id), chr(key).upper())
                Clock.schedule_once(set_grid_block_to_default, 1)
            else:
                self.text = "X"
                self.background_normal = DEFAULT_ATLAS
                self.background_color = 1, 0, 0, 1
                Clock.schedule_once(not_correct_letter, 1)

    # @kivy_timing -> Slow
    def fade_effect(self, *_) -> None:
        if self.opacity < 1:
            self.opacity += 0.1
        # Unregister event after use
        elif self.opacity > 1:
            Clock.unschedule(self.fade_effect_ptr)
