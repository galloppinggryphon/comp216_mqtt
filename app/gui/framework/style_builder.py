from dataclasses import dataclass
from tkinter.ttk import Style
from typing import (Any, Literal, Optional,  Tuple, )

# type TWidgets = Literal[
#     "Button",
#     "Checkbutton",
#     "Combobox",
#     "Entry",
#     "Frame",
#     "Labelframe",
#     "Label",
#     "Menubutton",
#     "Notebook",
#     "Panedwindow",
#     "Progressbar",
#     "Radiobutton",
#     "Scale",
#     "Scrollbar",
#     "Separator",
#     "Sizegrip",
#     "Spinbox",
#     "Treeview",
#     "OptionMenu",
# ]

type ConditionTypes = Literal["disabled", "pressed", "hover"]
type ConditionTypesNegated = Literal["!disabled", "!pressed", "!hover"]
type TConditions = Literal[
    "disabled", "pressed", "hover", "!disabled", "!pressed", "!hover"
]
type TValue = str
type TConditionList = list[TConditions]

@dataclass
class WidgetTypes:
    Button = "TButton"
    Checkbutton = "TCheckbutton"
    Combobox = "TCombobox"
    Entry = "TEntry"
    Frame = "TFrame"
    Labelframe = "TLabelframe"
    Label = "TLabel"
    Menubutton = "TMenubutton"
    Notebook = "TNotebook"
    Panedwindow = "TPanedwindow"
    Progressbar = "TProgressbar"
    Radiobutton = "TRadiobutton"
    Scale = "TScale"
    Scrollbar = "TScrollbar"
    Separator = "TSeparator"
    Sizegrip = "TSizegrip"
    Spinbox = "TSpinbox"
    Treeview = "TTreeview"
    OptionMenu = "TOptionMenu"



class StyleBuilder:
    __indent_level = 0
    styles: dict[str, dict[str, Any]]
    conditions: dict[str, dict[str, list[Tuple[TConditionList, TValue]]]]
    current_widget = ""
    tk_style: Style

    def __init__(self, style: Style):
        self.tk_style = style
        self.styles = {}
        self.conditions = {}

    def __enter__(self):
        if self.__indent_level > 2:
            raise TypeError('Max two levels!')

        if self.__indent_level == 1 and not self.current_widget:
            raise TypeError('Widget not defined!')

        self.__indent_level += 1
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.current_widget = ""
        self.__indent_level -= 1

    def widget(self, widget: str, variant: Optional[str] = None):
        self.current_widget = widget
        if variant:
            self.current_widget = f"{variant}.{widget}"
        return self

    def style(self, **rules):
        self.styles[self.current_widget] = rules


    def conditional(self, **conditions: list[Tuple[TConditionList, TValue]]):
        if not self.current_widget:
            raise TypeError('Widget not defined!')

        self.conditions[self.current_widget] = conditions

    def apply(self):
        for widget in self.styles:
            self.tk_style.configure(
                widget,
                **self.styles[widget]
            )

            if widget in self.conditions:
                self.tk_style.map(
                    widget,
                    **self.conditions[widget]
                )
