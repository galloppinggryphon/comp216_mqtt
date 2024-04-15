from app.config.theme_config import ThemeConfig
from app.gui.framework.window_config import WindowConfig

main_window_config = WindowConfig(
    window_title="COMP216 MQTT Project",
    header_title="MQTT Control Panel",
    width=700,
    height=500,
    background=ThemeConfig.background_colour
)

client_window_1 = WindowConfig(
    window_title="Client 1 - COMP216 MQTT Project",
    header_title="Client 1",
    width=800,
    height=800,
    background=ThemeConfig.background_colour
)

client_window_2 = WindowConfig(
    window_title="Client 2 - COMP216 MQTT Project",
    header_title="Client 2",
    width=800,
    height=600,
    background=ThemeConfig.background_colour
)
device_window_1 = WindowConfig(
    window_title="Device Config - COMP216 MQTT Project",
    header_title="Configure Device",
    width=800,
    height=550,
    background=ThemeConfig.background_colour
)
