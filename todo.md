# TODO

## Devices configs (mqtt_config.py)

`- `Configure three devices
  - Locations: maybe outdoor (done) + living_room, bed_room?
  - Clone existing, add to `device_config` list
  - Data must be _"random with a pattern"_ - use the brownian generator (random with direction)

## Simulation

- Move publisher initialization from `main.py` to `IoTSimulator.py`
  - Devices should probably be registered the first time they are started (in `start_publisher()`)
- Publisher error conditions (extras) - probably handle in `payload_simulator.py`
  - Skip blocks
  - Transmit "wild data"
- `save_device_config` handler: callback to send to the device config window, triggered when saved
  - Handle saving changed settings - update device_config.device\_\* in mqtt_config.

## Client windows

- Create two different client windows

### Client 2:

- Add client 2 in `window_configs.py`
- Duplicate client window 1
- Configure `__init__` -> super(): `super().__init__(False, window_configs.client_window_2, theme_config.ThemeConfig, theme_config.window_styles)`
- completed task.

### Both clients

- Add subscribers
- Create layout
- On_message callbacks
  - Update GUI
  - Handle error conditions

### Main window

- About button

---

## Assignment checklist

- [x] Broker

### Publisher

- [ ] Publisher GUI
  - [ ] Change settings
- [x] Configure and run multiple publishers
- [x] Random data with pattern
- [x] Data generator
- [x] Packaging data
  - [x] As JSON
  - [x] With timestamp
- [x] Submit data to broker
  - [x] With topic
  - [x] Missed transmissions
- [ ] Extras
  - [ ] Skip blocks
  - [ ] Transmit wild data
  - [x] Value added (point out in video, e.g. configuration object, diagrams)

### Subscriber

- [x] Configure and run multiple subscribers
- [x] Receiving data
  - [x] Receive from broker
  - [x] Decode data
- [ ] Handle data
  - [ ] Display data as text
  - [ ] Display data visually
  - [ ] Handle erroneous data
  - [ ] Handle missing data

### Other

- [ ] Code quality
- [ ] Video demo
