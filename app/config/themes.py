from dataclasses import dataclass
from tkinter.ttk import Style

@dataclass
class ThemeConfig:
    theme = "clam"
    primary_bg_colour = "#e0f7fa"
    primary_fg_colour = "#37474f"
    secondary_bg_colour = "#b2dfdb"
    background_colour = ("",)
    default_font = ("Arial", 12)
    header_font = ("Arial", 20, "bold")
    canvas_config = {"background": "#e0f7fa"}


#TTK Style() configuration
#Note: this must be a function, it has to be executed after tk() has been initialized
def window_style():
    style = Style()
    style.theme_use(ThemeConfig.theme)

    default_font = ThemeConfig.default_font
    header_font = ThemeConfig.header_font

    # Default style
    style.configure(
        ".",
        background=ThemeConfig.primary_bg_colour,
        foreground=ThemeConfig.primary_fg_colour,
        font=default_font,
    )
    style.configure("TLabel", font=ThemeConfig.default_font)
    style.configure("Header.TFrame",
                    background=ThemeConfig.secondary_bg_colour)
    style.configure(
        "Header.TLabel", background=ThemeConfig.secondary_bg_colour, font=header_font
    )
    style.configure("TEntry", padding=(4), bd=4,
                    font=ThemeConfig.default_font, foreground="black")
    style.configure(
        "TButton",
        padding=(3),
        bd=0,
        font=default_font,
        background="white",
        foreground="black",
    )
    style.configure("TRadiobutton", padding=(3))

    return style
