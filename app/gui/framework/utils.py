import colorsys

def clamp(num, min_val, max_val):
    return max(min_val, min(num, max_val))

def rgb_to_hex(*rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def hex_to_rgb(hex: str):
    _hex = hex.lstrip("#")
    return [
        int(_hex[i : i + 2], 16) for i in (0, 2, 4)
    ]  # alt method tuple(map(ord,hexcode[1:].decode('hex')))

def _tint_or_shade(hex: str, tint_modifier: float = -1, shade_modifier: float = -1):
    # Normalize values to 0-1
    rgb = [(x / 255) for x in list(hex_to_rgb(hex))]
    h, l, s = colorsys.rgb_to_hls(*rgb)

    if tint_modifier >= 0:
        l = l / (1 - tint_modifier)
    elif shade_modifier >= 0:
        l = l * (1 - shade_modifier)

    l = clamp(l, 0, 1)
    rgb = [round(i * 255) for i in colorsys.hls_to_rgb(h, l, s)]

    # Normalize to 0-255
    return rgb_to_hex(*rgb)


def tint(hex: str, modifier: float = -1):
    return _tint_or_shade(hex, tint_modifier=modifier)


def shade(hex: str, modifier: float = 1):
    return _tint_or_shade(hex, shade_modifier=modifier)


def luminosity(hex: str, luminosity: int):
    rgb = [(x / 255) for x in list(hex_to_rgb(hex))]
    h, l, s = colorsys.rgb_to_hls(*rgb)
    l = luminosity / 100
    l = clamp(l, 0, 1)
    rgb = [round(i * 255) for i in colorsys.hls_to_rgb(h, l, s)]
    return rgb_to_hex(*rgb)
