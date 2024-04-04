from tkinter import Tk, NSEW, EW
from tkinter.ttk import Style, Frame, Label
from typing import Callable

from app.config.themes import ThemeConfig
from app.gui.framework.window_config import WindowConfig


class TKWindow:
    window_config: WindowConfig
    main_pane: Frame
    top_pane: Frame
    bottom_pane: Frame
    x: str

    def __init__(self, config: WindowConfig, theme: ThemeConfig, window_style: Callable[..., Style]):
        super().__init__()

        self.window = Tk()
        window_style()

        self.window_config = config
        self.window_setup()

    def window_setup(self):
        w, h, title, background = (
            self.window_config.width,
            self.window_config.height,
            self.window_config.window_title,
            self.window_config.background,
        )

        win = self.window
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.config(bg=background)

        win.grid_columnconfigure(0, weight=1)
        win.grid_rowconfigure(0, weight=1)  # top_pane
        win.grid_rowconfigure(1, weight=5)  # main_pane
        win.grid_rowconfigure(2, weight=1)  # bottom_pane

        self.draw_layout()

    def draw_layout(self):
        self.draw_header()
        self.draw_main()
        self.draw_action_pane()

    def draw_header(self):
        top_pane = Frame(self.window, padding=10, style="Header.TFrame")
        top_pane.grid(row=0, column=0, sticky=NSEW)
        Label(
            top_pane, text=self.window_config.header_title, style="Header.TLabel"
        ).pack(expand=True)

        self.top_pane = top_pane

    def draw_main(self):
        main_pane = Frame(self.window)
        main_pane.grid(row=1, column=0, pady=20, padx=10, sticky=NSEW)
        self.main_pane = main_pane

    def draw_action_pane(self):
        bottom_pane = Frame(self.window)
        bottom_pane.columnconfigure(0, weight=4)
        bottom_pane.columnconfigure(1, weight=1)
        bottom_pane.columnconfigure(2, weight=1)
        bottom_pane.columnconfigure(3, weight=4)
        bottom_pane.grid(row=2, pady=10, sticky=EW)

        self.bottom_pane = bottom_pane

    def mainloop(self):
        self.window.mainloop()
