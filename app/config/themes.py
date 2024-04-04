from dataclasses import dataclass
from tkinter.ttk import Style

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
    style.theme_use(theme)

    default_font = default_font
    header_font = header_font

    # Default style
    style.configure(
        ".",
        background=primary_bg_colour,
        foreground=primary_fg_colour,
        font=default_font,
    )
    style.configure("TLabel", font=default_font)
    style.configure("Header.TFrame",
                    background=secondary_bg_colour)
    style.configure(
        "Header.TLabel", background=secondary_bg_colour, font=header_font
    )
    style.configure("TEntry", padding=(4), bd=4,
                    font=default_font, foreground="black")
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
