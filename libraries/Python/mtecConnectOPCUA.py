from opcua import Client, ua #https://github.com/FreeOpcUa/python-opcua

class Machine:
    def __init__(self, baseNode="ns=4;s=|var|B-Fortis CC-Slim S04.Application.GVL_OPC.", liveBitNode = "Livebit2machine"):
        self.baseNode = baseNode
        self.liveBitNode = liveBitNode

    """Connects to the machine using the provided IP
    Args:
        ip: IP-Adress of the machine
    """
    def connect(self, ip):
        self.reader = Client(ip)
        self.writer = Client(ip)
        self.reader.connect()
        self.writer.connect()
        self.reader.load_type_definitions()
        self.writer.load_type_definitions()
        self.subscribe("Livebit2extern", self.changeLivebit, 500)
    
    """Changes the value of a OPCUA Variable
    Args:
        variable: Variable to change
        value: value to change the variable to
        typ: string of variable type (bool, int, float)
    """
    def change(self, parameter, value, typ):
        #print(parameter, value, typ)
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
        self.writer.get_node(self.baseNode + parameter).set_value(ua.Variant(value, t))

    """Reades the value of a OPCUA Variable
    Args:
        variable: Variable to read
    """
    def read(self, parameter):
        return self.reader.get_node(self.baseNode + parameter).get_value()

    """Subscribes to given parameter
    Args:
        parameter: the OPC-UA Parameter to subscribe to (check docs for names)
        callback: Callback the variable and timestamp gets passed - callb(value, parameter)
        intervall: Intervall in ms that defined the frequency in which the parameter is checked
    """
    def subscribe(self, parameter, callback, intervall):
        subscriptionHandler = OpcuaSubscriptionHandler(parameter, callback)
        subscription = self.reader.create_subscription(intervall, subscriptionHandler)
        handler = subscription.subscribe_data_change(self.reader.get_node(self.baseNode + parameter))
        return [subscription, handler]

    """Changes the Livebit
    Args:
        value: The value to change the Livebit to
    """
    def changeLivebit(self, value, parameter=None):
        self.change(self.liveBitNode, value, "bool")





class Mixingpump(Machine):
    """Starts / Stops the machine
    Args / returns:
        state: true/false = on/off
    """
    @property
    def running(self):
        return self.read("Remote_start")
    @running.setter
    def running(self, state):
        self.change("Remote_start", state, "bool")
    
    """Changes / reads the speed setting of the mixingpump
    Args / returns:
        speed: Speed in %
    """
    @property
    def speed(self):
        return self.read("set_value_mixingpump")*100/65535 # 100% = 65535, 0% = 0
    @speed.setter
    def speed(self, speed):
        hz = speed*65535/100 # 100% = 65535, 0% = 0
        self.change("set_value_mixingpump", int(hz), "uint16")
    
    """Reads the real speed of the mixingpump
    Returns:
        Speed in %
    """
    @property
    def real_speed(self):
        speed = self.read("actual_value_mixingpump")
        return speed*100/65535 # 100% = 65535, 0% = 0

    """Starts / Stops the dosingpump
    Args / returns:
        state: true/false = on/off
    """
    @property
    def dosingpump(self):
        return self.read("state_dosingpump_on")
    @dosingpump.setter
    def dosingpump(self, state):
        self.change("state_dosingpump_on", state, "bool")

    """Changes / reads the speed setting of the dosingpump
    Args / returns:
        speed: Speed in %
    """
    @property
    def dosingspeed(self):
        return self.read("set_value_dosingpump")
    @dosingspeed.setter
    def dosingspeed(self, speed):
        self.change("set_value_dosingpump", int(speed), "float")

    """Changes / reads the water setting of the mixingpump
    Args / returns:
        speed: amount in l/h
    """
    @property
    def water(self):
        return self.read("set_value_water_flow")
    @water.setter
    def water(self, speed):
        self.change("set_value_water_flow", float(speed), "float")

    """Reads the real amount of water
    Returns:
        Amount in l/H
    """
    @property
    def real_water(self):
        return self.read("actual_value_water_flow")
    
    """Reads the real temperature of the water
    Returns:
        Temperature in °C
    """



    @property
    def real_water_temperature(self):
        return self.read("actual_value_water_temp")
    
    """Reads the real temperature of the mortar
    Returns:
        Temperature in °C
    """
    @property
    def real_temperature(self):
        return self.read("actual_value_mat_temp")

    """Reads the real pressure of the mortar
    Returns:
        Pressure in bar
    """
    @property
    def real_pressure(self):
        return self.read("actual_value_pressure")

    """Reads if machine is in error state
    Returns:
        is error? (true/false)
    """
    @property
    def error(self):
        return self.read("error")
    
    """Reads the error number of the machine
    Returns:
        error number (0 = none)
    """
    @property
    def error_no(self):
        return self.read("error_no")

    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation (true/false)
    """
    @property
    def ready(self):
        return self.read("Ready_for_operation")

    """Checks if the mixer is running (in automatic mode)
    Returns:
        mixer running
    """
    @property
    def mixing(self):
        return self.read("aut_mixer")

    """Checks if the mixingpump is running
    Returns:
        mixingpump is running (true/false)
    """
    @property
    def pumping(self):
        return self.pumping_net or self.pumping_fc

    """Checks if the mixingpump is running on power supply (in automatic mode)
    Returns:
        mixingpump is running on power supply (true/false)
    """
    @property
    def pumping_net(self):
        return self.read("aut_mixingpump_net")

    """Checks if the mixingpump is running on frequency converter supply (in automatic mode)
    Returns:
        mixingpump is running on frequency converter supply (true/false)
    """
    @property
    def pumping_fc(self):
        return self.read("aut_mixingpump_fc")

    """Checks if the selenoid valve is open (in automatic mode)
    Returns:
        selenoid valve is open (true/false)
    """
    @property
    def solenoidvalve(self):
        return self.read("aut_solenoid_valve")
    
    """Checks if the water pump is running (in automatic mode)
    Returns:
        waterpump is running (true/false)
    """
    @property
    def waterpump(self):
        return self.read("aut_waterpump")

    """Checks if remote is connected
    Returns:
        remote is connected (true/false)
    """
    @property
    def remote(self):
        return self.read("Remote_connected")



    """Changes the state of a Digital Output
    Args:
        pin: Pin number (1 - 8)
        value: true/fale = high/low
    """
    def setDigital(self, pin, value):
        if pin < 1 or pin > 8:
            print("Pin number (" + str(pin) + ") out of range (1 - 8)")
            return 
        self.change("reserve_DO_" + str(pin), value, "bool")
    """Reads the state of a Digital Input
    Args:
        pin: Pin number (1 - 10)
    Returns:
        actual value (true / false)
    """
    def getDigital(self, pin):
        if pin < 1 or pin > 10:
            print("Pin number (" + str(pin) + ") out of range (1 - 10)")
            return
        return self.read("reserve_DI_" + str(pin))

    """Changes the state of a Analog Output
    Args:
        pin: Pin number (1 - 2)
        value: value to set 0 to 65535
    """
    def setAnalog(self, pin, value):
        if pin < 1 or pin > 2:
            print("Pin number (" + str(pin) + ") out of range (1 - 2)")
            return 
        self.change("reserve_AO_" + str(pin), value, "uint16")
    """Reads the state of a Analog Input
    Args:
        pin: Pin number (1 - 5)
    Returns:
        actual value (0 - 65535)
    """
    def getAnalog(self, pin):
        if pin < 1 or pin > 5:
            print("Pin number (" + str(pin) + ") out of range (1 - 5)")
            return
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
        self.speed = speed
    def getSpeed(self):
        return self.real_speed/2 # return in Hz (100% = 50Hz)
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
        state: true/false = on/off
    """
    @property
    def running(self):
        return self.read("state_printhead_on")
    @running.setter
    def running(self, state):
        self.change("state_printhead_on", state, "bool")

    """Changes / reads the speed setting of the printhead
    Args / returns:
        speed: Speed in 1/min
    """
    @property
    def speed(self):
        return self.read("set_value_printhead")
    @speed.setter
    def speed(self, speed):
        self.change("set_value_printhead", int(speed), "uint16")

    """Reads the real speed of the printhead
    Returns:
        Speed in 1/min
    """
    @property
    def real_speed(self):
        return self.read("actual_value_printhead")
    
    """Starts / Stops the cleaning water
    Args / returns:
        state: true/false = on/off
    """
    @property
    def cleaning(self):
        return self.read("state_solenoid_valve")
    @cleaning.setter
    def cleaning(self, state):
        self.change("state_solenoid_valve", state, "bool")

    """Reads the real pressure of the printhead
    Returns:
        Pressure in bar
    """
    @property
    def real_pressure(self):
        return self.read("actual_value_pressure_printhead")
    
    """Reads if machine is in error state
    Returns:
        is error? (true/false)
    """
    @property
    def error(self):
        return self.read("error_printhead")
    
    """Reads the error number of the machine
    Returns:
        error number (0 = none)
    """
    @property
    def error_no(self):
        return self.read("error_no_printhead")
    
    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation (true/false)
    """
    @property
    def ready(self):
        return self.read("Ready_for_operation_printhead")





class Dosingpump(Machine):
    """Starts / Stops the dosingpump
    Args / returns:
        state: true/false = on/off
    """
    @property
    def running(self):
        return self.read("state_dosingpump_on")
    @running.setter
    def running(self, state):
        self.change("state_dosingpump_on", state, "bool")
    
    """Changes / reads the speed setting of the dosingpump
    Args / returns:
        speed: Speed in ml/min
    """
    @property
    def speed(self):
        return self.read("set_value_additive")
    @speed.setter
    def speed(self, speed):
        self.change("set_value_additive", int(speed), "float")

    """Reads the real speed of the dosingpump
    Returns:
        Speed in ml/min
    """
    @property
    def real_speed(self):
        return self.read("actual_value_additive")
    
    """Reads the real pressure of the dosingpump
    Returns:
        Pressure in bar
    """
    @property
    def real_pressure(self):
        return self.read("actual_value_pressure_dosingpump")

    """Reads if machine is in error state
    Returns:
        is error? (true/false)
    """
    @property
    def error(self):
        return self.read("error_dosingpump")
    
    """Reads the error number of the machine
    Returns:
        error number (0 = none)
    """
    @property
    def error_no(self):
        return self.read("error_no_dosingpump")
    
    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation (true/false)
    """
    @property
    def ready(self):
        return self.read("Ready_for_operation_dosingpump")





class OpcuaSubscriptionHandler:

    def __init__(self, parameter, callback):
        self.parameter = parameter
        self.callback = callback

    def datachange_notification(self, node, value, data):
        self.callback(value, self.parameter)
