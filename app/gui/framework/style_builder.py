from copy import copy, deepcopy
from dataclasses import dataclass
import logging
import pprint
from tkinter.ttk import Style
from typing import (Any, Literal, Optional,  Tuple, reveal_type, )

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

type TValidTkStates = Literal[
    "active", "disabled", "pressed", "hover", "selected", "focus", "readonly", "!active", "!disabled", "!pressed", "!hover", "!selected", "!focus", "!readonly"
]
type TValue = str
type TValidTkStateList = list[TValidTkStates]


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
    __level = 0
    styles: dict[str, dict[str, Any]]
    states: dict[str, dict[str,
                           dict[Tuple[TValidTkStates, ...] | TValidTkStates, TValue]]]
    current_widget = ""
    tk_style: Style

    def __init__(self, style: Style):
        self.tk_style = style
        self.styles = {}
        self.states = {}

    def __enter__(self):
        if self.__level > 1:
            logging.error(
                "StyleBuilder() error: Invalid `with` context, max two levels of nesting supported.")
            return self

        if self.__level == 1 and not self.current_widget:
            logging.error(
                'StyleBuilder() error: no `widget` has been set for the current context.')
            return self

        self.__level += 1
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.current_widget = ""
        self.__level -= 1

    def widget(self, widget: str, variant: Optional[str] = None):
        self.current_widget = widget
        if variant:
            self.current_widget = f"{variant}.{widget}"
        return self

    def style(self, **rules):
        widget = self.current_widget
        if not widget in self.styles:
            self.styles[widget] = rules
        else:
            for key in rules:
                self.styles[widget][key] = rules[key]

    def map(self, **states: dict[Tuple[TValidTkStates, ...] | TValidTkStates, TValue]):
        widget = self.current_widget
        if not widget in self.states:
            self.states[widget] = states
        else:
            props = self.states[widget]

            for prop_name in states:
                if prop_name in props:
                    props[prop_name].update(states[prop_name])
                else:
                    props[prop_name] = states[prop_name]

    def extend(self, widget: str):
        if not widget in self.styles and not widget in self.states:
            logging.error(f"StyleBuilder() error: Cannot extend style '{
                          widget}' - style not defined.")
            return

        if widget in self.styles:
            self.styles[self.current_widget] = deepcopy(self.styles[widget])

        if widget in self.states:
            self.states[self.current_widget] = deepcopy(self.states[widget])

    def apply(self):
        for widget in self.styles:
            self.tk_style.configure(
                widget,
                **self.styles[widget]
            )

            if not widget in self.states:
                continue

            # Massage state data into right form: { property_name=[ (state, ..., property_value), ... ], ... }
            tk_states = {}
            for prop_name in self.states[widget]:
                tk_states[prop_name] = []
                props = self.states[widget][prop_name]
                for state_keys in props:
                    state_tpl = state_keys if isinstance(
                        state_keys, tuple) else (state_keys,)

                    value = props[state_keys]
                    if value is not None:
                        tk_states[prop_name].append(state_tpl + (value,))

            self.tk_style.map(
                widget,
                **tk_states
            )
