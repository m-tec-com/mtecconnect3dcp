# mtecconnect3dcp Python Library

This library provides a simple interface to connect and control m-tec machines via OPC UA and Modbus. It supports different machine types such as Mixingpump (duo-mix 3DCP (+), SMP 3DCP), Printhead (flow-matic PX), Dosingpump (flow-matic) via OPC-UA, and Pumps (P20, P50) via Modbus.

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
mp.running = True  # Start the mixingpump

# Connect to a Printhead
ph = Printhead()
ph.connect("opc.tcp://<FLOW-MATIC_IP>:4840")
ph.speed = 1000  # Set speed to 1000 1/min
ph.running = True  # Start the printhead

# Connect to a Dosingpump
dp = Dosingpump()
dp.connect("opc.tcp://<FLOW-MATIC_IP>:4840")
dp.speed = 30  # Set speed to 30 ml/min
dp.running = True  # Start the dosingpump

# Connect to a Pump (P20/P50 via Modbus)
pump = Pump()
pump.connect(port="COM7")
pump.speed = 25  # Set speed to 25Hz
pump.running = True  # Start the pump
```

## Supported Properties and Functions by Machine

### Control

| Function/Property         | Get | Set | Type         | Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|-----|-----|--------------|------------------------------------|------|---------|----------|-----|------------|-----------|
| running                  |  :white_check_mark:  |  :white_check_mark:  | bool         | Start/stop machine                 |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| reverse                  |  :white_check_mark:  |  :white_check_mark:  | bool         | Set/Get running reverse   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
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
| real_speed               | float        | speed              |           |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| real_pressure            | float        | pressure           | bar       |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :white_check_mark:   |  :white_check_mark: (optional)   |
| real_water               | float        | water flow         | l/h       |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| real_water_temperature   | float        | water temperature  | °C        |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| real_temperature         | float        | mortar temperature | °C        |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |
| silolevel                | float        | Silo level         | %         |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| getDigital(pin)          | function     | Digital input      | bool      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| getAnalog(pin)           | function     | Analog input       | 0 - 65535 |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| voltage                  | bool         | Voltage            |           |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| current                  | bool         | Current            |           |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |
| torque                   | bool         | Torque             |           |  :white_check_mark:   |  :x:   |  :x:   |  :x:   |  :x:   |  :x:   |



### Status (GET)

| Function/Property        | Type         | Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|--------------|------------------------------------|------|---------|----------|-----|------------|-----------|
| error                    | bool         | error state                    |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| error_no                 | int          | error number                   |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| ready                    | bool         | Ready for operation            |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |
| mixing                   | bool         | mixing                         |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| pumping                  | bool         | pumping                        |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| pumping_net              | bool         | pumping via net                |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| pumping_fc               | bool         | pumping via FC                 |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| remote                   | bool         | hardware remote connected      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| solenoidvalve            | bool         | solenoid valve open            |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| waterpump                | bool         | pumping waterpump running      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |
| rotaryvalve              | bool         | rotary valve running           |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| compressor               | bool         | compressor running             |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |
| vibrator                 | (bool, bool) | vibrator running (vib1, vib2)  |  :x:   |  :x:   |  :x:   |  :white_check_mark:   |  :x:   |  :x:   |

### Subscriptions

| Function/Property        | Type         | Description                        | Pump (P20 & P50)| duo-mix 3DCP | duo-mix 3DCP+ | SMP 3DCP | Dosingpump (flow-matic PX) | Printhead (flow-matic PX) |
|--------------------------|--------------|------------------------------------|------|---------|----------|-----|------------|-----------|
| subscribe(var, cb, ms)   | function     | Subscribe to variable changes      |  :x:   |  :white_check_mark:   |  :white_check_mark:   |  :white_check_mark:   |  :x:   |  :x:   |

You can subscribe to OPC UA variables for real-time updates:

```python
def callback(value, parameter):
    print(f"{parameter} changed to {value}")

mp.subscribe("Livebit2extern", callback, 500)  # Check every 500 ms
```

Check the OPC-UA description provided by m-tec for all information about all variables and their names.

---
