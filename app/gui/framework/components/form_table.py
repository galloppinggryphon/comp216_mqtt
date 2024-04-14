import logging
import tkinter as tk
from tkinter import BaseWidget, Toplevel, Tk
from tkinter.ttk import Frame


class FormTable:
    __level = 0
    table: Frame
    parent: Frame | Toplevel | Tk
    num_rows: int
    current_row = 0
    rows: list[Frame]
    settings: dict

    def __init__(self, parent: Frame | Toplevel | Tk, rows: int, settings: dict = ...):
        self.settings = {
            "pad_y": 10,
            "sticky": tk.NSEW,
            "padding": 10,
            "style": ""
        }
        if settings is not ...:
            self.settings.update(settings)

        self.parent = parent
        self.num_rows = rows
        self.rows = []
        self.table = Frame(self.parent, style=self.settings["style"], padding=self.settings["padding"])
        self.draw()

    def __enter__(self):
        if self.__level > 1:
            logging.error(
                "Form() error: Invalid `with` context, max two levels of nesting supported.")
            return self

        if self.__level == 1 and not self.current_widget:
            logging.error(
                'Form() error: not in a row().')
            return self

        self.__level += 1
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.current_widget = ""
        self.__level -= 1

    def draw(self):
        table = self.table
        table.grid_columnconfigure(0, uniform="1", weight=1)
        table.grid_columnconfigure(1, uniform="1", weight=1)
        table.grid_rowconfigure(self.num_rows)

    def addRow(self):
        self.current_row += 1
        row = self.Row(self.table, self.current_row, self.settings)

        return row

    class Row:
        __form: Frame
        __col1: BaseWidget = ...
        __col2: BaseWidget = ...
        __row: int
        __settings: dict

        def __init__(self, table: Frame, row: int, settings: dict):
            self.__form = table
            self.__row = row
            self.__settings = settings

        @property
        def col1(self):
            return self.__col1

        @col1.setter
        def col1(self, value: BaseWidget):
            self.__col1 = value
            self.__col1.grid(column=0, row=self.__row, sticky=self.__settings["sticky"], pady=self.__settings["pad_y"])

        @property
        def col2(self):
            return self.__col2

        @col2.setter
        def col2(self, value: BaseWidget):
            self.__col2 = value
            self.__col2.grid(column=1, row=self.__row, sticky=self.__settings["sticky"], pady=self.__settings["pad_y"])

        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            ...

        def __call__(self):
            return self.__form
