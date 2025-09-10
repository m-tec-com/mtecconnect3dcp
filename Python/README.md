# mtecconnect3dcp Python Library

This library provides a simple interface to connect and control m-tec machines via OPC UA. It supports different machine types such as Mixingpump (duo-mix 3DCP (+), SMP 3DCP (+)), Printhead (flow-matic PX), and Dosingpump (flow-matic).

## Installation


1. Install this library:

```
pip install mtecconnect3dcp
```


### Example
See `/Python/example.py` for a full example. Below is a minimal usage guide:

```python
from mtecconnect3dcp import Mixingpump, Printhead, Dosingpump

# Connect to a Mixingpump
mp = Mixingpump()
mp.connect("opc.tcp://<MIXINGPUMP_IP>:4840")
mp.speed = 50  # Set speed to 50%
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
```

### Common Properties and Methods

#### Mixingpump
- `mp.running` (bool): Start/stop the mixingpump
- `mp.speed` (int, Hz): Set speed ( :warning: 20 - 50)
- `mp.real_speed` (float, Hz): Get actual speed
- `mp.dosingpump` (bool): Start/stop dosingpump
- `mp.dosingspeed` (float): Set dosingpump speed
- `mp.water` (float): Set water flow (l/h)
- `mp.real_water` (float): Get actual water flow (l/h)
- `mp.real_water_temperature` (float): Get water temperature (°C)
- `mp.real_temperature` (float): Get mortar temperature (°C)
- `mp.real_pressure` (float): Get pressure (bar)
- `mp.error` (bool): Get Error state
- `mp.error_no` (int): Get Error number
- `mp.ready` (bool): Get Ready for operation

#### Printhead
- `ph.running` (bool): Start/stop the printhead
- `ph.speed` (float, 1/min): Set speed
- `ph.real_speed` (float, 1/min): Get actual speed
- `ph.cleaning` (bool): Start/stop cleaning water
- `ph.real_pressure` (float): Get pressure (bar) (if optional sensor installed)
- `ph.error` (bool): Get Error state
- `ph.error_no` (int): Get Error number
- `ph.ready` (bool): Get Ready for operation

#### Dosingpump
- `dp.running` (bool): Start/stop the dosingpump
- `dp.speed` (float): Set speed (ml/min)
- `dp.real_speed` (float): Get actual speed (ml/min)
- `dp.real_pressure` (float): Get pressure (bar)
- `dp.error` (bool): Get Error state
- `dp.error_no` (int): Get Error number
- `dp.ready` (bool): Get Ready for operation

### Digital and Analog I/O (Mixingpump)
- `mp.setDigital(pin, value)`: Set digital output (pin 1-8)
- `mp.getDigital(pin)`: Read digital input (pin 1-10)
- `mp.setAnalog(pin, value)`: Set analog output (pin 1-2, value 0-65535)
- `mp.getAnalog(pin)`: Read analog input (pin 1-5)

### Subscriptions
You can subscribe to OPC UA variables for real-time updates:

```python
def callback(value, parameter):
    print(f"{parameter} changed to {value}")

mp.subscribe("Livebit2extern", callback, 500)  # Check every 500 ms
```

Check the OPC-UA description provided by m-tec for all information about all variables and their names.
