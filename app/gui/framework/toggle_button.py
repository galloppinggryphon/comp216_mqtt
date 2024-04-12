import logging
from tkinter import Event
from tkinter.ttk import Button
from typing import Optional, Callable

from app.gui.framework.super_init import super_init

# Hello
type TToggleCallback = Callable[[bool, bool, Optional[bool], Optional[Event]], bool]
'''- Callback arguments: function(current_toggle_state: bool, new_toggle_state: bool, event: Event|None, is_virtual_event: bool|None).
- Must return new toggle state.
'''

class ToggleButton(Button):
    """ToggleButton based on ttk.Button.

    Example:
    ```
    toggle = ToggleButton(text="Toggle Button!")
    toggle.on_toggle()
    ```
    """
    _virtual_event: str
    _on_toggle_on: TToggleCallback|None = None
    _on_toggle_off: TToggleCallback|None = None
    _allow_toggle_on: bool
    _allow_toggle_off: bool

    __init__ = super_init(Button.__init__)

    @property
    def is_toggled(self):
        return 'selected' in self.state()

    def toggle(self):
        self._toggle()

    def _toggle(self, set_toggled: Optional[bool] = None, is_virtual_event: Optional[bool] = False, event: Optional[Event] = None):
        # If set_toggled is defined, set current state to its inverse
        # is_toggled = self.is_toggled if set_toggled is None else not set_toggled
        new_toggle_state = set_toggled if set_toggled is not None else not self.is_toggled

        logging.info(f'Button toggled (new state: {new_toggle_state})')

        if new_toggle_state and self._on_toggle_on:
            new_toggle_state = self._on_toggle_on(self.is_toggled, new_toggle_state, event, is_virtual_event)
        elif not new_toggle_state and self._on_toggle_off:
            new_toggle_state = self._on_toggle_off(self.is_toggled, new_toggle_state, event, is_virtual_event)

        if new_toggle_state:
            self.state(['selected'])
        else:
            self.state(['!selected'])



        # if is_toggled:
        #     if self._allow_toggle_off or is_virtual_event:
        #         self.state(['!selected'])
        #         logging.info('Should be toggled off')

        #         if self._on_toggle_off:
        #             self._on_toggle_off()
        # else:
        #     if self._allow_toggle_on or is_virtual_event:
        #         self.state(['selected'])

        #         if self._on_toggle_on:
        #             self._on_toggle_on()

    def off(self):
        self._toggle(False)

    def on(self):
        self._toggle(True)

    def on_toggle(self, toggle_callback: Optional[TToggleCallback] = None, toggle_on_callback: Optional[TToggleCallback] = None, toggle_off_callback: Optional[TToggleCallback] = None, allow_toggle_on: bool = True, allow_toggle_off: bool = True,   bind_to: str | list[str] = "<Button-1>", virtual: str = "<<toggle_button>>"):
        _bind_to = bind_to if isinstance(bind_to, list) else [bind_to]

        self._allow_toggle_on = allow_toggle_on
        self._allow_toggle_off = allow_toggle_off

        if toggle_callback:
            self._on_toggle_on = toggle_callback
            self._on_toggle_off = toggle_callback
        else:
            if toggle_on_callback:
                self._on_toggle_on = toggle_on_callback
            if toggle_off_callback:
                self._on_toggle_off = toggle_off_callback

        if virtual:
            self._virtual_event = virtual
            self.event_add(virtual, 'None')
            _bind_to.append(virtual)

        # Built-in events
        for key in _bind_to:
            self.bind(key, self._toggle_handler, "%d")  # type: ignore

    def trigger_toggle(self, new_state: Optional[bool] = None):
        logging.info('Trigger toggle')
        Event.event_data = { "new_state": None if new_state is None else new_state } # type: ignore
        self.event_generate(self._virtual_event)

    def _toggle_handler(self, event: Optional[Event] = None):
        print('Toggledigoggleti -->', self.is_toggled, event)
        set_toggled = None
        is_virtual_event = False

        if event and 'event_data' in Event.__dict__ and Event.__dict__['event_data'] is not None:
            set_toggled = Event.event_data['new_state'] # type: ignore
            is_virtual_event = True
            Event.event_data = None # type: ignore

        self._toggle(is_virtual_event = is_virtual_event, set_toggled = set_toggled, event = event)
