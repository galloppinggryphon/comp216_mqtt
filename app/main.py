# from app.gui.main_window import MainWindow

from app.api.data_generator import DataGenerator
from app.helpers.iterable_class import IterableClass
from app.config import theme_config

class Main:
    def __init__(self):
        # app = MainWindow(main_window_config, ThemeConfig, window_style)

        data_gen = DataGenerator('brownian', value_range=(0,100), count=20, decimals=0)
        print(data_gen.values)


if __name__ == '__main__':
    Main()
