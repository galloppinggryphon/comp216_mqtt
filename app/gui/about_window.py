import logging
import tkinter as tk
from tkinter.ttk import Frame, Label
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs

spacing_y = 10
spacing_x = 10

class AboutWindow(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.about_window, theme_config.ThemeConfig, theme_config.window_styles)
        logging.info(f"Opened About Window")
        self.draw_main_section()

    def draw_main_section(self):
        frame = Frame(self.main, padding=10)
        frame.pack(expand=True, fill=tk.BOTH)

        Label(frame, text="A project in COMP216", style="H2.TLabel").pack(pady=(0,20))
        Label(frame, text="Centennial College, Toronto").pack()
        Label(frame, text="Winter, 2024").pack()
        Label(frame, text="Created by:", style="H3.TLabel", ).pack(pady=(20,5))
        Label(frame, text="Atefeh Arabi - @atefeharabi").pack()
        Label(frame, text="Amanda Simire - @amandasimire").pack()
        Label(frame, text="Bjornar Egede-Nissen - @galloppinggryphon").pack()
        Label(frame, text="Ruolan Wang - @ruolan89").pack()
