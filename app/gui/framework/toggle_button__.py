from tkinter.ttk import Button
from typing import Any, Callable, Optional


class ToggleButton(Button):
    _virtual_key: str
    _on_toggle: Callable

    @property
    def is_toggled(self):
        return 'selected' in self.state()

    def toggle(self):
        if self.is_toggled:
            self.off()
        else:
            self.on()

    def off(self):
        self.state(['!selected'])

    def on(self):
        self.state(['selected'])

    def on_toggle(self, callback: Optional[Callable[..., None]] = None, bind_to: str | list[str] = "<Button-1>", virtual: str = "<<toggle_button>>"):
        def _handler(data):
            print('Toggledigoggleti -->', self.is_toggled)
            self.toggle()
            if callback:
                callback(data)

        _bind_to = bind_to if isinstance(bind_to, list) else [bind_to]

        if virtual:
            self._virtual_key = virtual
            self.event_add(virtual, 'None')
            _bind_to.append(virtual)

        # Built-in events
        for key in _bind_to:
            self.bind(key, _handler, "%d")  # type: ignore
