import logging
import tkinter as tk
from tkinter import BaseWidget, Toplevel, Tk
from tkinter.ttk import Frame


class FormTable:
    __level = 0
    frame: Frame
    parent: Frame | Toplevel | Tk
    num_rows: int
    current_row = 0
    rows: list[Frame]
    settings: dict

    def __init__(self, parent: Frame | Toplevel | Tk, rows: int, settings: dict = ...):
        self.settings = {
            "sticky": tk.NSEW,
            "padding": 10,
            "style": "",
            "col_spacing": 10,
            "row_spacing": 10
        }
        if settings is not ...:
            self.settings.update(settings)

        self.parent = parent
        self.num_rows = rows
        self.rows = []
        self.frame = Frame(self.parent, style=self.settings["style"], padding=self.settings["padding"])
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
        table = self.frame
        table.grid_columnconfigure(0, uniform="1", weight=1)
        table.grid_columnconfigure(1, uniform="1", weight=1)
        table.grid_rowconfigure(self.num_rows)

    def addRow(self):
        self.current_row += 1
        row = self.Row(self.frame, self.current_row, self.settings)

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
        def col1(self, widget: BaseWidget):
            self.__col1 = widget
            self.__place_col(0, widget)

        @property
        def col2(self):
            return self.__col2

        @col2.setter
        def col2(self, widget: BaseWidget):
            self.__col2 = widget
            self.__place_col(1, widget)

        def __place_col(self, col: int, widget: BaseWidget):
            col_spacing, row_spacing = self.__settings["col_spacing"], self.__settings["row_spacing"]
            padx = (0, col_spacing) if col == 0 else 0
            pady=(row_spacing/2, row_spacing/2)
            widget.grid(column=col, row=self.__row, sticky=self.__settings["sticky"], padx=padx, pady=pady)

        def __enter__(self):
            return self

        def __exit__(self, exception_type, exception_value, traceback):
            ...

        def __call__(self):
            return self.__form
