from __future__ import annotations
from queue import Queue
from tkinter import Tk, NSEW, EW, Toplevel, Event, EventType
from tkinter.ttk import Style, Frame, Label
from typing import Any, Callable, Optional, Type, final

from app.config.theme_config import ThemeConfig
from app.gui.framework.event_data import EventData
from app.gui.framework.window_config import WindowConfig


class TKWindow:
    """Wrapper around tk()/toplevel(). Provides scaffolding for configuration and GUI setup.

    Creates a window with three rows (panes):
    - TKWindow.top: narrow, mainly header
    - TKWindow.main: middle section, main content
    - TKWindow.bottom: narrow, for action buttons, navigation, other

    """
    style: Style
    window_config: WindowConfig
    theme: Type[ThemeConfig]
    window_close_callbacks: list[Callable]
    __main: Frame
    __top: Frame
    __bottom: Frame
    __header: Label

    @property
    def header(self):
        return self.__header
    @property
    def top(self):
        return self.__top

    @property
    def main(self):
        return self.__main

    @property
    def bottom(self):
        return self.__bottom

    def __init__(self, root: bool, config: WindowConfig, theme: type[ThemeConfig], window_styles: Optional[Callable] = None):
        super().__init__()
        self.window_config = config
        self.theme = theme
        self.window_close_callbacks = []

        # Create window and apply styles
        if root:
            self.window = Tk()
            self.style = Style()
            if window_styles:
                # self.window.after(10, window_styles)
                self.style = window_styles(Style())

        else:
            self.window = Toplevel()

        self._window_setup()
        self._on_window_close()

    def _window_setup(self):
        conf = self.window_config

        w, h, title, background = (
            conf.width,
            conf.height,
            conf.window_title,
            conf.background,
        )

        win = self.window
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.config(bg=background)  # type: ignore

        win.grid_columnconfigure(0, weight=1)
        win.grid_rowconfigure(0, weight=1)  # top_pane
        win.grid_rowconfigure(1, weight=5)  # main_pane
        win.grid_rowconfigure(2, weight=1)  # bottom_pane

        self._draw_header()
        self._draw_main()
        self._draw_action_pane()

    def _draw_header(self):
        top_pane = Frame(self.window, padding=10, style="HeaderPanel.TFrame")
        top_pane.grid(row=0, column=0, sticky=NSEW)
        self.__header = Label(
            top_pane, text=self.window_config.header_title, style="H1.TLabel"  # type: ignore
        )
        self.__header.pack(expand=True)
        self.__top = top_pane

    def _draw_main(self):
        main_pane = Frame(self.window)
        main_pane.grid(row=1, column=0, pady=20, padx=10, sticky=NSEW)
        self.__main = main_pane

    def _draw_action_pane(self):
        bottom_pane = Frame(self.window)
        bottom_pane.columnconfigure(0, weight=4)
        bottom_pane.columnconfigure(1, weight=1)
        bottom_pane.columnconfigure(2, weight=1)
        bottom_pane.columnconfigure(3, weight=4)
        bottom_pane.grid(row=2, pady=10, sticky=EW)

        self.__bottom = bottom_pane


    def bind_event(self, event: EventType, callback: Callable):
        """
        Bind control events (keyboard, mouse, focus, etc) or virtual events to a callback.
        """
        event_key = f"<{event}>"
        self.window.bind(event_key, callback)

    def bind_virtual_event(self, event_name: str, callback: Callable, return_trigger = False):
        event_key = f"<<{event_name}>>"
        self.window.event_add(event_key, 'None')
        self.window.bind(event_key, callback)

        if return_trigger:
            return self.create_virtual_event_trigger(event_name)

    def trigger_virtual_event(self, event_name: str,  data: Optional[Any] = None):
        if data is not None:
            EventData.set(id(self), event_name, data)
        self.window.event_generate(f"<<{event_name}>>")

    def create_virtual_event_trigger(self, event_name: str):
        def trigger(data: Optional[Any] = None):
            self.trigger_virtual_event(event_name, data)
        return trigger

    def mainloop(self):
        self.window.mainloop()

    def close(self):
        for callback in self.window_close_callbacks:
            callback(self)
        self.window.destroy()

    def on_window_close(self, callback: Callable):
        self.window_close_callbacks.append(callback)

    def _on_window_close(self):
        def _on_close():
            for callback in self.window_close_callbacks:
                callback(self)
            self.window.destroy()

        self.window.protocol('WM_DELETE_WINDOW', _on_close)

    def is_window_open(self):
        return self.window.winfo_exists()

    def modal(self):
        self.window.wait_visibility()
        self.window.grab_set()
        return self
        # self.window.transient(parent)

    def resizable(self, horizontal = True, vertical = True):
        self.window.resizable(horizontal,vertical)
        return self
