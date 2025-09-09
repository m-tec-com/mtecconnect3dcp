from asyncua.sync import Client, SyncNode
from asyncua import ua #https://github.com/FreeOpcUa/asyncua

class Machine:
    """Initializes the Machine class
    Args:
        baseNode: str; Base node of the machine
        liveBitNode: str; Name of the livebit variable (default = "Livebit2machine")
    """
    def __init__(self, baseNode = "ns=4;s=|var|B-Fortis CC-Slim S04.Application.GVL_OPC.", liveBitNode = "Livebit2machine"):
        self.baseNode = baseNode
        self.liveBitNode = liveBitNode

    """Connects to the machine using the provided IP
    Args:
        ip: str; IP-Adress of the machine
    """
    def connect(self, ip: str):
        self.reader = Client(url=ip)
        self.writer = Client(url=ip)
        self.reader.connect()
        self.writer.connect()
        self.reader.load_data_type_definitions()
        self.writer.load_data_type_definitions()
        self.subscribe("Livebit2extern", self.changeLivebit, 500)
    
    """Changes the value of a OPCUA Variable
    Args:
        parameter: str; Variable to change
        value: any; value to change the variable to
        typ: str; string of variable type (bool, uint16, int32, float)
    """
    def change(self, parameter: str, value: any, typ: str):
        if typ == "bool":
            t = ua.VariantType.Boolean
            value = bool(value)
        elif typ == "uint16":
            t = ua.VariantType.UInt16
            value = int(abs(value))
        elif typ == "int32":
            t = ua.VariantType.Int32
            value = int(value)
        elif typ == "float":
            t = ua.VariantType.Float
            value = float(value)
        else:
            return
        node = self.writer.get_node(self.baseNode + parameter)
        node.set_value(ua.Variant(value, t))

    """Reades the value of a OPCUA Variable
    Args:
        variable: str; Variable to read
    """
    def read(self, parameter: str) -> any:
        node = self.reader.get_node(self.baseNode + parameter)
        return node.get_value()

    """Subscribes to given parameter
    Args:
        parameter: str; the OPC-UA Parameter to subscribe to (check docs for names)
        callback: callable; Callback the variable and timestamp gets passed - callb(value, parameter)
        interval: int; Interval in ms that defined the frequency in which the parameter is checked
    """
    def subscribe(self, parameter: str, callback: callable, interval: int):
        subscriptionHandler = OpcuaSubscriptionHandler(parameter, callback)
        subscription = self.reader.create_subscription(interval, subscriptionHandler)
        handler = subscription.subscribe_data_change(self.reader.get_node(self.baseNode + parameter))
        return [subscription, handler]

    """Changes the Livebit
    Args:
        value: bool; The value to change the Livebit to
    """
    def changeLivebit(self, value: bool, parameter=None):
        self.change(self.liveBitNode, value, "bool")





class Mixingpump(Machine):
    """Starts / Stops the machine
    Args / returns:
        state: bool; true/false = on/off
    """
    @property
    def running(self) -> bool:
        return bool(self.read("Remote_start"))
    @running.setter
    def running(self, state: bool):
        self.change("Remote_start", state, "bool")
    
    """Changes / reads the speed setting of the mixingpump
    Args / returns:
        speed: float; Speed in Hz
    """
    @property
    def speed(self) -> float:
        return (self.read("set_value_mixingpump") * 30) / 65535 + 20 # 50Hz = 65535, 20Hz
    @speed.setter
    def speed(self, speed: float):
        if speed < 20:
            raise ValueError("Speed in Hz cannot be below 20")
        if speed > 50:
            raise ValueError("Speed in Hz cannot be above 50")
        hz = (speed-20) * 65535 / 30 # 50Hz = 65535, 20Hz = 0
        self.change("set_value_mixingpump", int(hz), "uint16")
    
    """Reads the real speed of the mixingpump
    Returns:
        speed: float; Speed in Hz
    """
    @property
    def real_speed(self) -> float:
        speed = self.read("actual_value_mixingpump")
        return speed * 50 / 65535 # 50Hz = 65535, 0Hz = 0

    """Starts / Stops the dosingpump
    Args / returns:
        state: bool; true/false = on/off
    """
    @property
    def dosingpump(self) -> bool:
        return bool(self.read("state_dosingpump_on"))
    @dosingpump.setter
    def dosingpump(self, state: bool):
        self.change("state_dosingpump_on", state, "bool")

    """Changes / reads the speed setting of the dosingpump
    Args / returns:
        speed: float; Speed in %
    """
    @property
    def dosingspeed(self) -> float:
        return self.read("set_value_dosingpump")
    @dosingspeed.setter
    def dosingspeed(self, speed: float):
        self.change("set_value_dosingpump", float(speed), "float")

    """Changes / reads the water setting of the mixingpump
    Args / returns:
        speed: float; amount in l/h
    """
    @property
    def water(self) -> float:
        return self.read("set_value_water_flow")
    @water.setter
    def water(self, speed: float):
        self.change("set_value_water_flow", float(speed), "float")

    """Reads the real amount of water
    Returns:
        speed: float; amount in l/H
    """
    @property
    def real_water(self) -> float:
        return float(self.read("actual_value_water_flow"))
    
    """Reads the real temperature of the water
    Returns:
        temperature: float; Temperature in °C
    """
    @property
    def real_water_temperature(self) -> float:
        return float(self.read("actual_value_water_temp"))

    """Reads the real temperature of the mortar
    Returns:
        temperature: float; Temperature in °C
    """
    @property
    def real_temperature(self) -> float:
        return float(self.read("actual_value_mat_temp"))

    """Reads the real pressure of the mortar
    Returns:
        pressure: float; Pressure in bar
    """
    @property
    def real_pressure(self) -> float:
        return float(self.read("actual_value_pressure"))

    """Reads if machine is in error state
    Returns:
        is error: bool
    """
    @property
    def error(self) -> bool:
        return self.read("error")
    
    """Reads the error number of the machine
    Returns:
        error number: int; (0 = none)
    """
    @property
    def error_no(self) -> int:
        return self.read("error_no")

    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation: bool
    """
    @property
    def ready(self) -> bool:
        return self.read("Ready_for_operation")

    """Checks if the mixer is running (in automatic mode)
    Returns:
        mixer running: bool
    """
    @property
    def mixing(self) -> bool:
        return self.read("aut_mixer")

    """Checks if the mixingpump is running
    Returns:
        mixingpump is running: bool
    """
    @property
    def pumping(self) -> bool:
        return self.pumping_net or self.pumping_fc

    """Checks if the mixingpump is running on power supply (in automatic mode)
    Returns:
        mixingpump is running on power supply: bool
    """
    @property
    def pumping_net(self) -> bool:
        return self.read("aut_mixingpump_net")

    """Checks if the mixingpump is running on frequency converter supply (in automatic mode)
    Returns:
        mixingpump is running on frequency converter supply: bool
    """
    @property
    def pumping_fc(self) -> bool:
        return self.read("aut_mixingpump_fc")

    """Checks if the selenoid valve is open (in automatic mode)
    Returns:
        selenoid valve is open: bool
    """
    @property
    def solenoidvalve(self) -> bool:
        return self.read("aut_solenoid_valve")
    
    """Checks if the water pump is running (in automatic mode)
    Returns:
        waterpump is running: bool
    """
    @property
    def waterpump(self) -> bool:
        return self.read("aut_waterpump")

    """Checks if remote is connected
    Returns:
        remote is connected: bool
    """
    @property
    def remote(self) -> bool:
        return self.read("Remote_connected")



    """Changes the state of a Digital Output
    Args:
        pin: int; Pin number (1 - 8)
        value: bool; true/false = high/low
    """
    def setDigital(self, pin: int, value: bool):
        if pin < 1 or pin > 8:
            raise ValueError(f"Pin number ({pin}) out of range (1 - 8)")
        self.change("reserve_DO_" + str(pin), value, "bool")
    """Reads the state of a Digital Input
    Args:
        pin: int; Pin number (1 - 10)
    Returns:
        actual value: bool; true/false = high/low
    """
    def getDigital(self, pin: int) -> bool:
        if pin < 1 or pin > 10:
            raise ValueError(f"Pin number ({pin}) out of range (1 - 10)")
        return self.read("reserve_DI_" + str(pin))

    """Changes the state of a Analog Output
    Args:
        pin: int; Pin number (1 - 2)
        value: int; value to set 0 to 65535
    """
    def setAnalog(self, pin: int, value: int):
        if pin < 1 or pin > 2:
            raise ValueError(f"Pin number ({pin}) out of range (1 - 2)")
        self.change("reserve_AO_" + str(pin), value, "uint16")
    """Reads the state of a Analog Input
    Args:
        pin: int; Pin number (1 - 5)
    Returns:
        actual value: int; (0 - 65535)
    """
    def getAnalog(self, pin: int) -> int:
        if pin < 1 or pin > 5:
            raise ValueError(f"Pin number ({pin}) out of range (1 - 5)")
        return self.read("reserve_AI_" + str(pin))
    


    """Backward compatibility"""
    def start(self):
        self.running = True
    def stop(self):
        self.running = False
    def startDosingpump(self):
        self.dosingpump = True
    def stopDosingpump(self):
        self.dosingpump = False
    def setSpeedDosingpump(self, speed):
        self.dosingspeed = speed
    def setSpeed(self, speed):
        self.speed = speed * 30 / 100 + 20 # 100% = 50Hz, 0% = 20Hz
    def getSpeed(self):
        return self.real_speed
    def setWater(self, speed):
        self.water = speed
    def isError(self):
        return self.error
    def getError(self):
        return self.error_no
    def isReadyForOperation(self):
        return self.ready
    def isMixerRunning(self):
        return self.mixing
    def isMixingpumpRunningNet(self):
        return self.pumping_net
    def isMixingpumpRunningFc(self):
        return self.pumping_fc
    def isMixingpumpRunning(self):
        return self.pumping
    def isSolenoidValve(self):
        return self.solenoidvalve
    def isWaterpump(self):
        return self.waterpump
    def isRemote(self):
        return self.remote





class Printhead(Machine):
    """Starts / Stops the printhead
    Args / returns:
        state: bool; true/false = on/off
    """
    @property
    def running(self) -> bool:
        return self.read("state_printhead_on")
    @running.setter
    def running(self, state: bool):
        self.change("state_printhead_on", state, "bool")

    """Changes / reads the speed setting of the printhead
    Args / returns:
        speed: int; Speed in 1/min
    """
    @property
    def speed(self) -> float:
        return self.read("set_value_printhead")
    @speed.setter
    def speed(self, speed: float):
        self.change("set_value_printhead", float(speed), "float")

    """Reads the real speed of the printhead
    Returns:
        speed: int; Speed in 1/min
    """
    @property
    def real_speed(self) -> int:
        return self.read("actual_value_printhead")
    
    """Starts / Stops the cleaning water
    Args / returns:
        state: bool; true/false = on/off
    """
    @property
    def cleaning(self) -> bool:
        return self.read("state_solenoid_valve")
    @cleaning.setter
    def cleaning(self, state: bool):
        self.change("state_solenoid_valve", state, "bool")

    """Reads the real pressure of the printhead
    Returns:
        pressure: float; pressure in bar (if optional sensor installed)
    """
    @property
    def real_pressure(self) -> float:
        return self.read("actual_value_pressure_printhead")
    
    """Reads if machine is in error state
    Returns:
        is error: bool
    """
    @property
    def error(self) -> bool:
        return self.read("error_printhead")
    
    """Reads the error number of the machine
    Returns:
        error number: int; (0 = none)
    """
    @property
    def error_no(self) -> int:
        return self.read("error_no_printhead")
    
    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation: bool
    """
    @property
    def ready(self) -> bool:
        return self.read("Ready_for_operation_printhead")





class Dosingpump(Machine):
    """Starts / Stops the dosingpump
    Args / returns:
        state: bool; true/false = on/off
    """
    @property
    def running(self) -> bool:
        return self.read("state_dosingpump_on")
    @running.setter
    def running(self, state: bool):
        self.change("state_dosingpump_on", state, "bool")
    
    """Changes / reads the speed setting of the dosingpump
    Args / returns:
        speed: int; Speed in ml/min
    """
    @property
    def speed(self) -> float:
        return self.read("set_value_dosingpump")
    @speed.setter
    def speed(self, speed: float):
        self.change("set_value_dosingpump", float(speed), "float")

    """Reads the real speed of the dosingpump
    Returns:
        speed: int; Speed in ml/min
    """
    @property
    def real_speed(self) -> int:
        return self.read("actual_value_additive")
    
    """Reads the real pressure of the dosingpump
    Returns:
        pressure: float; Pressure in bar
    """
    @property
    def real_pressure(self) -> float:
        return self.read("actual_value_pressure_dosingpump")

    """Reads if machine is in error state
    Returns:
        is error: bool
    """
    @property
    def error(self) -> bool:
        return self.read("error_dosingpump")
    
    """Reads the error number of the machine
    Returns:
        error number: int; (0 = none)
    """
    @property
    def error_no(self) -> int:
        return self.read("error_no_dosingpump")
    
    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation: bool
    """
    @property
    def ready(self) -> bool:
        return self.read("Ready_for_operation_dosingpump")





class OpcuaSubscriptionHandler:

    def __init__(self, parameter, callback):
        self.parameter = parameter
        self.callback = callback

    def datachange_notification(self, node, value, data):
        self.callback(value, self.parameter)
