from app.config.theme_config import ThemeConfig
from app.config.mqtt_config import device_config
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
    height=600,
    background=ThemeConfig.background_colour
)

device_window_1 = WindowConfig(
    window_title="Device 1 - COMP216 MQTT Project",
    header_title=f"Configure {device_config[0].name} (#1)",
    width=800,
    height=600,
    background=ThemeConfig.background_colour
)
