from tkinter.ttk import Button
from app.gui.framework.tkwindow import TKWindow
from app.config import theme_config, window_configs

class DeviceWindow1(TKWindow):
    def __init__(self):
        super().__init__(False, window_configs.client_window_1, theme_config.ThemeConfig, theme_config.window_styles)
        self.main_section()

    def main_section(self):
        main = self.main
        Button(main, text="Device 1").grid(row=0, column=2)
