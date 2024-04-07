from collections.abc import Iterable, Mapping
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Style
from typing import (Literal,  Tuple, )

from app.helpers.config_base import ConfigBase
from app.helpers.utils import shade, tint


type Widgets = Literal[
    "Button",
    "Checkbutton",
    "Combobox",
    "Entry",
    "Frame",
    "Labelframe",
    "Label",
    "Menubutton",
    "Notebook",
    "Panedwindow",
    "Progressbar",
    "Radiobutton",
    "Scale",
    "Scrollbar",
    "Separator",
    "Sizegrip",
    "Spinbox",
    "Treeview",
    "OptionMenu",
]


class W:
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


def V(widget: W, variant: str):
    return f"{variant}.{widget}"


type ConditionTypes = Literal["disabled", "pressed", "hover"]
type ConditionTypesNegated = Literal["!disabled", "!pressed", "!hover"]
type TConditions = Literal[
    "disabled", "pressed", "hover", "!disabled", "!pressed", "!hover"
]
type TValue = str
type TConditionList = list[TConditions]


def Is(*condition: ConditionTypes | ConditionTypesNegated): ...


def Conditions0(**conditions: Tuple[Tuple[TConditionList, TValue], ...]):
    return conditions


def Conditions(**conditions: list[Tuple[TConditionList, TValue]]):
    return conditions


@dataclass
class ThemeConfig:
    theme = "default"  # "clam"

    primary = "#158cba"
    primary_complement = "black"
    secondary = "#919191"
    success = "#28b62c"
    info = "#75caeb"
    warning = "#ff851b"
    danger = "#ff4136"
    active = "#e5e5e5"

    main_bg_colour = "#e0f7fa"
    main_fg_colour = "#37474f"
    secondary_bg_colour = "#b2dfdb"
    background_colour = "#e0f7fa"
    default_font = ("Arial", 12)
    header_font = ("Arial", 20, "bold")
    canvas = {"background": "#e0f7fa"}
    # bootstrap = {
    #     "primary": "#158cba",
    #     "secondary": "#919191",
    #     "success": "#28b62c",
    #     "info": "#75caeb",
    #     "warning": "#ff851b",
    #     "danger": "#ff4136",
    #     "light": "#F6F6F6",
    #     "dark": "#555555",
    #     "bg": "#ffffff",
    #     "fg": "#555555",
    #     "selectbg": "#919191",
    #     "selectfg": "#ffffff",
    #     "border": "#ced4da",
    #     "inputfg": "#555555",
    #     "inputbg": "#fff",
    #     "active": "#e5e5e5",
    # }


def WindowStyles(style: Style):
    # style = Style()
    # style.theme_use(ThemeConfig.theme)

    TC = ThemeConfig

    def Button():
        NAME = W.Button

        class C:
            main = TC.main_bg_colour
            bordercolor = TC.main_bg_colour
            disabled_fg = shade(TC.primary, 0.5)
            disabled_bg = shade(TC.primary, 0.3)
            pressed = TC.warning
            hover = tint(TC.primary, 0.3)

        conditions = Conditions(
            bordercolor=[(["disabled"], C.bordercolor)],
            foreground=[(["disabled"], C.disabled_fg)],
            background=[
                (["disabled"], C.disabled_bg),
                (["pressed", "!disabled"], C.pressed),
                (["hover", "!disabled"], C.hover)
            ],
            darkcolor=[
                (["disabled"], C.disabled_bg),
                (["pressed", "!disabled"], C.pressed),
                (["hover", "!disabled"], C.hover)
            ],
            lightcolor=[
                (["disabled"], C.disabled_bg),
                (["pressed", "!disabled"], C.pressed),
                (["hover", "!disabled"], C.hover)
            ],
        )

        style.configure(
            NAME,
            bd=0,
            foreground="white",
            background=TC.primary,
            bordercolor=C.bordercolor,
            darkcolor=C.main,
            lightcolor=C.main,
            relief=tk.FLAT,
            focusthickness=0,
            focuscolor=C.main,
            padding=(10, 5),
            anchor=tk.CENTER,
        )

        style.map(
            NAME,
            **conditions
        )

    Button()


# TTK Style() configuration
# Note: this must be a function, it has to be executed after tk() has been initialized
def window_style():
    style = Style()
    style.theme_use(ThemeConfig.theme)

    WindowStyles(style)

    TC = ThemeConfig

    default_font = TC.default_font
    header_font = TC.header_font

    # Default style
    style.configure(
        ".",
        background=TC.main_bg_colour,
        foreground=TC.main_fg_colour,
        font=default_font,
    )
    style.configure("TLabel", font=default_font)
    style.configure("Header.TFrame", background=TC.secondary_bg_colour)
    style.configure(
        "Header.TLabel", background=TC.secondary_bg_colour, font=header_font
    )
    style.configure("TEntry", padding=(4), bd=4,
                    font=default_font, foreground="black")

    bordercolor = TC.main_bg_colour
    disabled_bg = (
        # Colors.make_transparent(0.10, self.colors.fg, self.colors.bg)
        TC.main_bg_colour
    )
    disabled_fg = (
        # Colors.make_transparent(0.30, self.colors.fg, self.colors.bg)
        TC.main_bg_colour
    )
    pressed = (
        # Colors.make_transparent(0.80, background, self.colors.bg)
        TC.main_bg_colour
    )
    hover = tint(
        TC.primary, 0.2
    )  # Colors.make_transparent(0.90, background, self.colors.bg)

    # style.configure(
    #     "TButton",
    #     bd=0,
    #     foreground="white",
    #     background=TC.primary,
    #     bordercolor=TC.main_bg_colour,
    #     darkcolor=TC.main_bg_colour,
    #     lightcolor=TC.main_bg_colour,
    #     # relief=tk.RAISED,
    #     relief=tk.FLAT,
    #     focusthickness=0,
    #     focuscolor=TC.main_bg_colour,
    #     padding=(10, 5),
    #     anchor=tk.CENTER,
    # )

    # style.map(
    #     "TButton",
    #     foreground=[("disabled", disabled_fg)],
    #     background=[
    #         ("disabled", disabled_bg),
    #         ("pressed !disabled", pressed),
    #         ("hover !disabled", hover),
    #     ],
    #     bordercolor=[("disabled", disabled_bg)],
    #     darkcolor=[
    #         ("disabled", disabled_bg),
    #         ("pressed !disabled", pressed),
    #         ("hover !disabled", hover),
    #     ],
    #     lightcolor=[
    #         ("disabled", disabled_bg),
    #         ("pressed !disabled", pressed),
    #         ("hover !disabled", hover),
    #     ],
    # )

    style.configure("TRadiobutton", padding=(3))

    return style
