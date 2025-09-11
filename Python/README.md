# mtecconnect3dcp Python Library

This library provides a simple interface to connect and control m-tec machines via OPC UA and Modbus. It supports different machine types such as Mixingpump (duo-mix 3DCP (+), SMP 3DCP), Printhead (flow-matic PX), Dosingpump (flow-matic) via OPC-UA, and Pumps (P20, P50) via Modbus.

## Entwicklerfreundlichkeit & IDE-Unterstützung

Diese Bibliothek verwendet ausführliche Python-Docstrings und Typannotationen. Dadurch werden in modernen IDEs wie Visual Studio Code automatische Tooltips, Autovervollständigung und Inline-Hilfen (IntelliSense) unterstützt. So erhalten Sie direkt beim Programmieren Hinweise zu Parametern, Rückgabewerten und Nutzung der Funktionen und Klassen.

**Hinweis:** Für das beste Erlebnis empfiehlt sich die Nutzung von VS Code oder einer anderen IDE mit Python-IntelliSense-Unterstützung.

## Installation


1. Install this library:

```
pip install mtecconnect3dcp
```


### Example
See `/Python/example.py` for a full example. Below is a minimal usage guide:

```python
from mtecconnect3dcp import Printhead, Dosingpump, Pump, Duomix, DuomixPlus, Smp

# Connect to a Mixingpump
mp = Duomix()
mp.connect("opc.tcp://<MIXINGPUMP_IP>:4840")
mp.speed = 50  # Set speed to 50Hz (20-50Hz range)
mp.run = True  # Start the mixingpump

# Connect to a Printhead
ph = Printhead()
ph.connect("opc.tcp://<FLOW-MATIC_IP>:4840")
ph.speed = 1000  # Set speed to 1000 1/min
ph.run = True  # Start the printhead

# Connect to a Dosingpump
dp = Dosingpump()
dp.connect("opc.tcp://<FLOW-MATIC_IP>:4840")
dp.speed = 30  # Set speed to 30 ml/min
dp.run = True  # Start the dosingpump

# Connect to a Pump (P20/P50 via Modbus)
pump = Pump()
pump.connect(port="COM7")
pump.speed = 25  # Set speed to 25Hz
pump.run = True  # Start the pump
```

## Supported Properties and Functions by Machine

### Control

| Function/Property         | Get | Set | Type         | Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|-----|-----|--------------|------------------------------------|------|---------|----------|-----|------------|-----------|
| run                      |  :white_check_mark:  |  :white_check_mark:  | bool         | Start/stop machine                 |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| reverse                  |  :white_check_mark:  |  :white_check_mark:  | bool         | Set/Get running reverse   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| emergcency_stop() |  :white_check_mark:  |  :x:  | function         | Execute Emergency Stop   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| speed                    |  :white_check_mark:  |  :white_check_mark:  | float/int    | Set/Get speed                      |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| dosingpump               |  :white_check_mark:  |  :white_check_mark:  | bool         | Start/stop dosingpump              |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| dosingspeed              |  :white_check_mark:  |  :white_check_mark:  | float        | Set dosingpump speed               |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| water                    |  :white_check_mark:  |  :white_check_mark:  | float        | Set water flow (l/h)               |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| cleaning                 |  :white_check_mark:  |  :white_check_mark:  | bool         | Start/stop cleaning water          |  :x:   |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |
| setDigital(pin, value)   |  :x:  |  :white_check_mark:  | function     | Set digital output                 |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| setAnalog(pin, value)    |  :x:  |  :white_check_mark:  | function     | Set analog output                  |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |

### Measure (GET)

| Function/Property        | Type         | Description        | Unit      | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|--------------|--------------------|-----------|-----------------|--------------|---------------|----------|----------------------------|---------------------------|
| m_speed               | float        | speed              |           |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| m_dosingspeed         | float        | speed of dosing pump | %       |  :x:   |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |
| m_pressure            | float        | pressure           | bar       |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :white_check_mark: (optional)   |
| m_water               | float        | water flow         | l/h       |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| m_water_temperature   | float        | water temperature  | °C        |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| m_temperature         | float        | mortar temperature | °C        |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| m_valve               | float        | valve position     | %         |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| m_silolevel           | float        | Silo level         | %         |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| m_voltage             | bool         | Voltage            |           |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| m_current             | bool         | Current            |           |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| m_torque              | bool         | Torque             |           |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| getDigital(pin)       | function     | Digital input      | bool      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| getAnalog(pin)        | function     | Analog input       | 0 - 65535 |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |



### Status (GET)

| Function/Property        | Type         | Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|--------------|------------------------------------|------|---------|----------|-----|------------|-----------|
| s_error                    | bool | error state                    |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| s_error_no                 | int  | error number                   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| s_ready                    | bool | Ready for operation            |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| s_mixing                   | bool | mixing                         |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_pumping                  | bool | pumping                        |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_pumping_net              | bool | pumping via net                |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_pumping_fc               | bool | pumping via FC                 |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_remote                   | bool | hardware remote connected      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| s_solenoidvalve            | bool | solenoid valve open            |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_waterpump                | bool | pumping waterpump running      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_emergency_stop           | bool | emergency stop ok              |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |
| s_on                       | bool | machine powered on             |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |
| s_safety_mp                | bool | mixingpump safety ok           |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_safety_mixer             | bool | mixer safety ok                |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_circuitbreaker_fc        | bool | Frequency Converter circuit breaker ok |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_circuitbreaker           | bool | other circuit breaker ok       |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_fc                       | bool | frequency converter ok         |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |
| s_operating_pressure       | bool | pressure ok                    |  :x:   |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |
| s_water_pressure           | bool | water pressure ok              |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_hopper_wet               | bool | wet material hopper ok         |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_hopper_dry               | bool | dry material hopper ok         |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_running_local            | bool | running in local mode          |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_phase_reversed           | bool | phase reversed                 |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_running                  | bool | Mixingpump running forward     |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |
| s_running_reverse          | bool | Mixingpump running reverse     |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| s_rotaryvalve              | bool | rotary valve running           |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_compressor               | bool | compressor running             |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_vibrator_1               | bool | vibrator 1 running             |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| s_vibrator_2               | bool | vibrator 2 running             |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |

### Subscriptions

| Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|------------------------------------|------|---------|----------|-----|------------|-----------|
| Subscribe to variable changes      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |

You can subscribe to OPC UA variables for real-time updates:

```python
def callback(value, parameter): # value and parameter (origial OPC-UA variable name) are optional
    print(f"{parameter} changed to {value}")
mp = Duomix()
mp.s_ready = callback # set a variable to you callback to subscribe
```
---
