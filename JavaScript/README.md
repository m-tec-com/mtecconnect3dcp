> :warning: &nbsp; This library is not perfect. Sometimes the returned values do not match with the requests if the communiction is fast.

&nbsp;

# Usage

## Minimal init

```html
<script src="mtecConnectModbus.js"></script>
<script>
    var pump = new mtecConnectModbus();

    async function connect() {
        await pump.connect();
     }
    
    async function start(){
        await (pump.speed = 20);
    }
    
    async function stop(){
        await pump.stop();
    }
</script>
<button onclick="connect()">Connect</button>
<button onclick="start()">Start</button>
<button onclick="stop()">Stop</button>
```
> :warning: &nbsp; Keep in mind:
> * `.connect()` has to be triggered by user gesture (e.g. onclick)
> * communication takes some time &rarr; use async functions and await

&nbsp;

## Documentation

### :wrench: &nbsp; :boom: &nbsp; constructor

Creates the Object to use the library.

```javascript
var pump = new mtecConnectModbus(inverterNumber);
```

parameters:
* string (length: 2), inverter number (parameter F802), optional (default: "01")

result:
* mtecConnectModbus, conatins everything used to communicate via modbus

&nbsp;

### :wrench: &nbsp; :electric_plug: &nbsp; connect

Connects to the serial converter.

> :memo: &nbsp; `.connect()` has to be triggered by user gesture (e.g. onclick)

```javascript
var connected = await pump.connect(); // has to be triggered by user gesture (e.g. onclick)
```

result:
* bool, connection to serial interface sucessful?

&nbsp;

### :gear: &nbsp; :arrows_counterclockwise: &nbsp; keep alive

> :memo: &nbsp; While the pump is running, a valid command has to be sent at least every second

If activated, the keep alive feature sends a command some time (interval) after the last command.

This feature can be tweaked in the settings:

* bool `pump.settings.keepAlive.active`, if keep alive feature is enabled, default: true
* int `pump.settings.keepAlive.interval`, interval after which the command is sent (in ms), default: 250
* string (or function with return string) `pump.settings.keepAlive.command` (length: 10), action number (2) + parameter number (4) + value (4), default: "03FD000001"
* function `pump.settings.keepAlive.callback`, gets called with return value as parameter, optional

&nbsp;

### :wrench: &nbsp; :arrow_forward: &nbsp; start & stop

Starts or stops the pump (target frequency has to be set)

```javascript
// target frequency has to be set
await pump.start();         // starts the pump
await pump.startReverse();  // starts the pump in reverse
await pump.stop();          // stops the pump
```

&nbsp;

### :pencil2: &nbsp; :timer_clock: &nbsp; set frequency

Sets the target frequency

```javascript
await (pump.frequency = frequency);
```

parameters:
* float, positive (resolution: 0.01), target frequency in Hz

&nbsp;

### :mag: &nbsp; :timer_clock: &nbsp; get frequency

Gets the actual frequency

```javascript
var frequency = await pump.frequency;
```

result:
* float, positive (resolution: 0.01), actual frequency in Hz

&nbsp;

### :pencil2: &nbsp; :fast_forward: &nbsp; set speed

Starts (or stops) the pump in the desired direction

> :warning: &nbsp; Do not switch between `set frequency` and `set speed`

```javascript
await (pump.speed = speed);
```

parameters:
* float, negative to reverse (resolution: 0.01), target frequency

&nbsp;

### :mag: &nbsp; :vertical_traffic_light: &nbsp; get ready

Gets the readiness of the machine (on)

```javascript
var ready = await pump.ready;
```

result:
* bool, machine is ready for operation

&nbsp;

### :mag: &nbsp; :zap: &nbsp; get voltage

Gets the actual output voltage

```javascript
var voltage = await pump.voltage;
```

result:
* float, positive (resolution: 0.01), actual voltage in % of voltage rating

&nbsp;

### :mag: &nbsp; :bulb: &nbsp; get current

Gets the actual output current

```javascript
var current = await pump.current;
```

result:
* float, positive (resolution: 0.01), actual voltage in % of current rating

&nbsp;

### :mag: &nbsp; :muscle: &nbsp; get torque

Gets the actual torque

```javascript
var torque = await pump.torque;
```

result:
* float, positive (resolution: 0.01), actual voltage in % of torque rating

&nbsp;

### :wrench: &nbsp; :hash: &nbsp; send custom command

Sends custom command to inverter

```javascript
var answer = await pump.sendCommand(parameter, value);
```

parameters:
* string (length: 6), action number (2) + parameter number (4), example: "03FD00"
* int, value

result:
* int, answer value (equals input value if write command)

&nbsp;