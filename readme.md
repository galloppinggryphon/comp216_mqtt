# COMP216 MQTT PROJECT

## Getting started with this repo

1.  Clone this repo: `git clone https://github.com/galloppinggryphon/comp216_mqtt.git`
2.  Open the `comp216_mqtt` folder and create a virtualenv: `python -m venv .venv`
3.  Install dependencies (Paho MQTT client):  `pip install -r requirements.txt`
4.  Install Eclipse Mosquitto broker: [https://mosquitto.org/](https://mosquitto.org/)

## Development aids for VSCode

**Extensions**:

- autopep8 (code formatter): [https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)
- isort (import assistance): [https://marketplace.visualstudio.com/items?itemName=ms-python.isort](https://marketplace.visualstudio.com/items?itemName=ms-python.isort)

Enable the formatter and isort in `.vscode/settings.json` (user or workspace) like this:

```
"[python]": {
    // (OPTIONAL) "editor.formatOnType": true,
    "editor.defaultFormatter": "ms-python.autopep8"
},
"python.analysis.autoImportCompletions": true
```

## Running

1.  Make sure mosquitto is running: `mosquitto` or `mosquitto -v` (verbose)
2.  Run `python main.py` in the `app` folder

# Resources

- Quick start (_not updated for v2_): [https://pypi.org/project/paho-mqtt/](https://pypi.org/project/paho-mqtt/)
- Full documentation: [https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html](https://eclipse.dev/paho/files/paho.mqtt.python/html/client.html)
- [http://www.steves-internet-guide.com/mqtt-python-callbacks/](http://www.steves-internet-guide.com/mqtt-python-callbacks/)
- [http://www.steves-internet-guide.com/python-mqtt-client-changes/](http://www.steves-internet-guide.com/python-mqtt-client-changes/)
- [http://www.steves-internet-guide.com/client-connections-python-mqtt/](http://www.steves-internet-guide.com/client-connections-python-mqtt/)

# Overview

### The project is organzied as implicit (anonymous/folder based) packages.

### Package structure:

```
app/
    api/
        helpers/
    config/
        device_data/
    gui/
        clients/
        devices/
        framework/
    helpers/
```

---

### Class overview

![Class overview](/diagrams/Class_overview.png)

### Broker

![MQTT overview](/diagrams/MQTT_diagram.png)
