from app.config.themes import ThemeConfig
from app.gui.framework.window_config import WindowConfig

main_window_config = WindowConfig(
    window_title="COMP216 MQTT Project",
    header_title="MQTT Control Panel",
    width=600,
    height=400,
    background=ThemeConfig.background_colour
)

client_window_1 = WindowConfig(
    window_title="Client 1 - COMP216 MQTT Project",
    header_title="Client 1",
    width=800,
    height=600,
    background=ThemeConfig.background_colour
)
