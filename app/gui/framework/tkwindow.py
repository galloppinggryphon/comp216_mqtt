from __future__ import annotations
from tkinter import Tk, NSEW, EW, Toplevel
from tkinter.ttk import Style, Frame, Label
from typing import Callable, Optional, Type

from app.config.themes import ThemeConfig
from app.gui.framework.window_config import WindowConfig


class TKWindow:
    """Wrapper around tk(). Provides scaffolding for configuration and GUI setup.

    Currently creates a window with three vertical sections (panes) that can be added to:
    - Top (narrow, mainly header)
    - Middle (main section)
    - Bottom (narrow, for buttons or other things)


    """
    window_config: WindowConfig
    theme: Type[ThemeConfig]
    main: Frame
    top: Frame
    bottom: Frame
    sub_windows: list

    def __init__(self, root: bool, config: WindowConfig, theme: type[ThemeConfig], window_style: Optional[Callable[..., Style]] = None):
        super().__init__()
        self.window_config = config
        self.theme = theme

        # Create window and apply styles
        if root:
            self.window = Tk()
            if window_style:
                self.window.after(10, window_style)
        else:
            self.window = Toplevel()


        self._window_setup()

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
        win.config(bg=background)

        win.grid_columnconfigure(0, weight=1)
        win.grid_rowconfigure(0, weight=1)  # top_pane
        win.grid_rowconfigure(1, weight=5)  # main_pane
        win.grid_rowconfigure(2, weight=1)  # bottom_pane

        self._draw_header()
        self._draw_main()
        self._draw_action_pane()

    def _draw_header(self):
        top_pane = Frame(self.window, padding=10, style="Header.TFrame")
        top_pane.grid(row=0, column=0, sticky=NSEW)
        Label(
            top_pane, text=self.window_config.header_title, style="Header.TLabel"
        ).pack(expand=True)
        self.top = top_pane

    def _draw_main(self):
        main_pane = Frame(self.window)
        main_pane.grid(row=1, column=0, pady=20, padx=10, sticky=NSEW)
        self.main = main_pane

    def _draw_action_pane(self):
        bottom_pane = Frame(self.window)
        bottom_pane.columnconfigure(0, weight=4)
        bottom_pane.columnconfigure(1, weight=1)
        bottom_pane.columnconfigure(2, weight=1)
        bottom_pane.columnconfigure(3, weight=4)
        bottom_pane.grid(row=2, pady=10, sticky=EW)

        self.bottom = bottom_pane


    def mainloop(self):
        self.window.mainloop()
