# mtecconnect3dcp Python Library

This library provides a simple interface to connect and control m-tec machines via OPC UA and Modbus. It supports different machine types such as Mixingpump (duo-mix 3DCP (+), SMP 3DCP), Printhead (flow-matic PX), Dosingpump (flow-matic) via OPC-UA, and Pumps (P20, P50) via Modbus.

## Developer Friendliness & IDE Support

This library uses comprehensive Python docstrings and type annotations. As a result, modern IDEs such as Visual Studio Code provide automatic tooltips, autocompletion, and inline help (IntelliSense). This gives you immediate guidance on parameters, return values, and usage of functions and classes while coding.

**Note:** For the best experience, it is recommended to use VS Code or another IDE with Python IntelliSense support.

## Installation


1. Install this library:

```
pip install mtecconnect3dcp
```


### Example
See `/Python/example.py` for an example of a print process. Below is a minimal usage guide:

```python
from mtecconnect3dcp import Printhead, Dosingpump, Pump, Duomix, DuomixPlus, Smp

# Connect to a m-tec connect duo-mix 3DCP
mp = Duomix()
mp.connect("10.129.4.73") # 10.129.4.73 is the default ip
mp.speed = 50  # Set speed to 50Hz (20-50Hz range)
mp.run = True  # Start the mixingpump

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
| run                      |  ✅  |  ✅  | bool         | Start/stop machine                 |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| reverse                  |  ✅  |  ✅  | bool         | Set/Get running reverse   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |  ❌   |
| emergcency_stop() |  ❌  |  ✅  | function         | Execute Emergency Stop   |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |  ❌   |
| speed                    |  ✅  |  ✅  | float/int    | Set/Get speed                      |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| dosingpump               |  ✅  |  ✅  | bool         | Start/stop dosingpump              |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| dosingspeed              |  ✅  |  ✅  | float        | Set dosingpump speed               |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| water                    |  ✅  |  ✅  | float        | Set water flow (l/h)               |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| cleaning                 |  ✅  |  ✅  | bool         | Start/stop cleaning water          |  ❌   |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |
| setDigital(pin, value)   |  ❌  |  ✅  | function     | Set digital output                 |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| setAnalog(pin, value)    |  ❌  |  ✅  | function     | Set analog output                  |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |

### Measure (GET)

| Function/Property        | Type         | Description        | Unit      | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|--------------|--------------------|-----------|-----------------|--------------|---------------|----------|----------------------------|---------------------------|
| m_speed               | float        | speed              |           |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| m_dosingspeed         | float        | speed of pump | %       |  ❌   |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |
| m_pressure            | float        | pressure           | bar       |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |  ✅ (optional)   |
| m_water               | float        | water flow         | l/h       |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| m_water_temperature   | float        | water temperature  | °C        |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| m_temperature         | float        | mortar temperature | °C        |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| m_valve               | float        | valve position     | %         |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| m_silolevel           | float        | Silo level         | %         |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |
| m_voltage             | bool         | Voltage            |           |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |  ❌   |
| m_current             | bool         | Current            |           |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |  ❌   |
| m_torque              | bool         | Torque             |           |  ✅   |  ❌   |  ❌   |  ❌   |  ❌   |  ❌   |
| getDigital(pin)       | function     | Digital input      | bool      |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| getAnalog(pin)        | function     | Analog input       | 0 - 65535 |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |



### Status (GET)

| Function/Property        | Type         | Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|--------------|------------------------------------|------|---------|----------|-----|------------|-----------|
| s_error                    | bool | error state                    |  ❌   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| s_error_no                 | int  | error number                   |  ❌   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| s_ready                    | bool | Ready for operation            |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| s_mixing                   | bool | mixing                         |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| s_pumping                  | bool | pumping                        |  ✅   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| s_pumping_forward          | bool | pumping forward                |  ✅   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_pumping_reverse          | bool | pumping reverse                |  ✅   |  ❌   |  ❔   |  ❌   |  ❌   |  ❌   |
| s_pumping_net              | bool | pumping via net                |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| s_pumping_fc               | bool | pumping via FC                 |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| s_remote                   | bool | hardware remote connected      |  ❌   |  ✅   |  ✅   |  ✅   |  ✅   |  ✅   |
| s_solenoidvalve            | bool | solenoid valve open            |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| s_waterpump                | bool | pumping waterpump running      |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |
| s_emergency_stop           | bool | emergency stop ok              |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |  ✅   |
| s_on                       | bool | machine powered on             |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |  ✅   |
| s_safety_mp                | bool | mixingpump safety ok           |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_safety_mixer             | bool | mixer safety ok                |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_circuitbreaker_fc        | bool | Frequency Converter circuit breaker ok |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_circuitbreaker           | bool | other circuit breaker ok       |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_fc                       | bool | frequency converter ok         |  ❌   |  ❌   |  ✅   |  ❌   |  ✅   |  ✅   |
| s_operating_pressure       | bool | pressure ok                    |  ❌   |  ❌   |  ❌   |  ❌   |  ✅   |  ✅   |
| s_water_pressure           | bool | water pressure ok              |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_hopper_wet               | bool | wet material hopper ok         |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_hopper_dry               | bool | dry material hopper ok         |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_running                  | bool | Machine running                |  ❌   |  ❌   |  ❌   |  ❌   |  ✅   |  ✅   |
| s_airpressure              | bool | airpressure ready              |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_phase_reversed           | bool | phase reversed                 |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |  ❌   |
| s_rotaryvalve              | bool | rotary valve running           |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |
| s_compressor               | bool | compressor running             |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |
| s_vibrator_1               | bool | vibrator 1 running             |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |
| s_vibrator_2               | bool | vibrator 2 running             |  ❌   |  ❌   |  ❌   |  ✅   |  ❌   |  ❌   |

### Subscriptions

| Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|------------------------------------|------|---------|----------|-----|------------|-----------|
| Subscribe to variable changes      |  ❌   |  ✅   |  ✅   |  ✅   |  ❌   |  ❌   |

You can subscribe to OPC UA variables for real-time updates:

```python
def callback(value, parameter, subscription): # value and parameter (origial OPC-UA variable name) are optional
    print(f"{parameter} changed to {value}")
    if value:
        print("we are ready to go")
        subscription.delete()
mp = Duomix()
mp.connect("10.129.4.73")
mp.s_ready = callback # set a variable to you callback to subscribe
```
---
