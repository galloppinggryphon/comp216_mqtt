from app.api.data_generator import DataGenerator
from app.gui.main_window import MainWindow
from app.helpers.iterable_class import IterableClass
from app.config import theme_config, main_window_config

class Main:
    def __init__(self):
        data_gen = DataGenerator('brownian', value_range=(0,100), count=20, decimals=0)
        print(data_gen.values)
        app = MainWindow(main_window_config, theme_config, theme_config.window_style)
        app.mainloop()


if __name__ == '__main__':
    Main()
