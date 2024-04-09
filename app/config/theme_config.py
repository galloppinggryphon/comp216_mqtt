from dataclasses import dataclass
from typing import Optional
import tkinter as tk
from tkinter.ttk import Style

from app.gui.framework.style_builder import StyleBuilder, WidgetTypes as W
from app.gui.framework.utils import shade, tint

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


# TTK Style() configuration
# Note: this must be a function, it has to be executed after tk() has been initialized
def window_styles(style: Optional[Style] = None):
    style = style if style else Style()
    style.theme_use(ThemeConfig.theme)

    TC = ThemeConfig

    default_font = TC.default_font
    header_font = TC.header_font
    main = TC.main_bg_colour

    with StyleBuilder(style) as S:
        with S.widget(".") as S:
            S.style(
                background=main,
                foreground=TC.main_fg_colour,
                font=default_font
            )

        with S.widget(W.Button) as S:
            bordercolor = main
            disabled_fg = shade(TC.primary, 0.5)
            disabled_bg = shade(TC.primary, 0.3)
            pressed = TC.warning
            hover = tint(TC.primary, 0.3)

            S.style(
                bd=0,
                foreground="white",
                background=TC.primary,
                bordercolor=bordercolor,
                darkcolor=main,
                lightcolor=main,
                relief=tk.FLAT,
                focusthickness=0,
                focuscolor=main,
                padding=(10, 5),
                anchor=tk.CENTER,
            )

            S.conditional(
                bordercolor=[(["disabled"], bordercolor)],
                foreground=[(["disabled"], disabled_fg)],
                background=[
                    (["disabled"], disabled_bg),
                    (["pressed", "!disabled"], pressed),
                    (["hover", "!disabled"], hover)
                ],
                darkcolor=[
                    (["disabled"], disabled_bg),
                    (["pressed", "!disabled"], pressed),
                    (["hover", "!disabled"], hover)
                ],
                lightcolor=[
                    (["disabled"], disabled_bg),
                    (["pressed", "!disabled"], pressed),
                    (["hover", "!disabled"], hover)
                ],
            )


        with S.widget(W.Button, "Primary") as S:
            bordercolor = TC.main_bg_colour
            disabled_fg = shade(TC.primary, 0.5)
            disabled_bg = shade(TC.primary, 0.3)
            pressed = TC.warning
            hover = tint(TC.primary, 0.3)

            S.style(
                bd=0,
                foreground="white",
                background=TC.primary,
                bordercolor=bordercolor,
                darkcolor=main,
                lightcolor=main,
                relief=tk.FLAT,
                focusthickness=0,
                focuscolor=main,
                padding=(10, 5),
                anchor=tk.CENTER,
            )

            S.conditional(
                bordercolor=[(["disabled"], bordercolor)],
                foreground=[(["disabled"], disabled_fg)],
                background=[
                    (["disabled"], disabled_bg),
                    (["pressed", "!disabled"], pressed),
                    (["hover", "!disabled"], hover)
                ],
                darkcolor=[
                    (["disabled"], disabled_bg),
                    (["pressed", "!disabled"], pressed),
                    (["hover", "!disabled"], hover)
                ],
                lightcolor=[
                    (["disabled"], disabled_bg),
                    (["pressed", "!disabled"], pressed),
                    (["hover", "!disabled"], hover)
                ],
            )

        with S.widget(W.Label, "Header") as S:
            S.style(
                background=TC.secondary_bg_colour,
                font=header_font
            )

        with S.widget(W.Label) as S:
            S.style(font=default_font)

        with S.widget(W.Frame, "Header") as S:
            S.style(background=TC.secondary_bg_colour)

        with S.widget(W.Frame, "Header") as S:
            S.style(background=TC.secondary_bg_colour)

        with S.widget(W.Entry) as S:
            S.style(
                padding=(4),
                bd=4,
                font=default_font,
                foreground="black"
            )

        # Apply styles
        S.apply()

    return style

# window_styles(Style())