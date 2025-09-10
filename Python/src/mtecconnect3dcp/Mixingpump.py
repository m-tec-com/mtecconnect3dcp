from .OPCUAMachine import OPCUAMachine

class Mixingpump(OPCUAMachine):
    """
    Class for controlling a mixing pump via OPC-UA.
    Inherits from OPCUAMachine.
    """
    @property
    def running(self) -> bool:
        """
        bool: True if the machine is running, False otherwise.
        """
        return bool(self.read("Remote_start"))
    @running.setter
    def running(self, state: bool):
        """
        Set the running state of the machine.

        Args:
            state (bool): True to start, False to stop.
        """
        self.change("Remote_start", state, "bool")

    @property
    def speed(self) -> float:
        """
        float: Speed setting of the mixingpump in Hz.
        """
        return (self.read("set_value_mixingpump") * 30) / 65535 + 20 # 50Hz = 65535, 20Hz
    @speed.setter
    def speed(self, speed: float):
        """
        Set the speed of the mixingpump.

        Args:
            speed (float): Speed in Hz (20-50).

        Raises:
            ValueError: If speed is out of range.
        """
        if speed < 20:
            raise ValueError("Speed in Hz cannot be below 20")
        if speed > 50:
            raise ValueError("Speed in Hz cannot be above 50")
        hz = (speed-20) * 65535 / 30 # 50Hz = 65535, 20Hz = 0
        self.change("set_value_mixingpump", int(hz), "uint16")

    @property
    def real_speed(self) -> float:
        """
        float: Real speed of the mixingpump in Hz.
        """
        speed = self.read("actual_value_mixingpump")
        return speed * 50 / 65535 # 50Hz = 65535, 0Hz = 0

    """Starts / Stops the dosingpump
    Args / returns:
        state: bool; true/false = on/off
    """
    @property
    def dosingpump(self) -> bool:
        """
        bool: True if the dosingpump is running, False otherwise.
        """
        return bool(self.safe_read("state_dosingpump_on", False))
    @dosingpump.setter
    def dosingpump(self, state: bool):
        """
        Set the running state of the dosingpump.

        Args:
            state (bool): True to start, False to stop.
        """
        self.safe_change("state_dosingpump_on", state, "bool")

    """Changes / reads the speed setting of the dosingpump
    Args / returns:
        speed: float; Speed in %
    """
    @property
    def dosingspeed(self) -> float:
        """
        float: Speed setting of the dosingpump in %.
        """
        return self.safe_read("set_value_dosingpump", 0.0)
    @dosingspeed.setter
    def dosingspeed(self, speed: float):
        """
        Set the speed of the dosingpump.

        Args:
            speed (float): Speed in %.
        """
        self.safe_change("set_value_dosingpump", float(speed), "float")

    """Changes / reads the water setting of the mixingpump
    Args / returns:
        speed: float; amount in l/h
    """
    @property
    def water(self) -> float:
        """
        float: Water setting of the mixingpump in l/h.
        """
        return self.safe_read("set_value_water_flow", 0.0)
    @water.setter
    def water(self, speed: float):
        """
        Set the water flow of the mixingpump.

        Args:
            speed (float): Amount in l/h.
        """
        self.safe_change("set_value_water_flow", float(speed), "float")

    """Reads the real amount of water
    Returns:
        speed: float; amount in l/H
    """
    @property
    def real_water(self) -> float:
        """
        float: Real amount of water in l/h.
        """
        return float(self.safe_read("actual_value_water_flow", 0.0))
    
    """Reads the real temperature of the water
    Returns:
        temperature: float; Temperature in °C
    """
    @property
    def real_water_temperature(self) -> float:
        """
        float: Real temperature of the water in °C.
        """
        return float(self.safe_read("actual_value_water_temp", 0.0))

    """Reads the real temperature of the mortar
    Returns:
        temperature: float; Temperature in °C
    """
    @property
    def real_temperature(self) -> float:
        """
        float: Real temperature of the mortar in °C.
        """
        return float(self.safe_read("actual_value_mat_temp", 0.0))

    """Reads the real pressure of the mortar
    Returns:
        pressure: float; Pressure in bar
    """
    @property
    def real_pressure(self) -> float:
        """
        float: Real pressure of the mortar in bar.
        """
        return float(self.safe_read("actual_value_pressure", 0.0))

    """Reads if machine is in error state
    Returns:
        is error: bool
    """
    @property
    def error(self) -> bool:
        """
        bool: True if the machine is in error state.
        """
        return self.read("error")
    
    """Reads the error number of the machine
    Returns:
        error number: int; (0 = none)
    """
    @property
    def error_no(self) -> int:
        """
        int: Error number of the machine (0 = none).
        """
        return self.read("error_no")

    """Checks if the machine is ready for operation (on, remote, mixer and mixingpump on)
    Returns:
        ready for operation: bool
    """
    @property
    def ready(self) -> bool:
        """
        bool: True if the machine is ready for operation.
        """
        return self.read("Ready_for_operation")

    """Checks if the mixer is running (in automatic mode)
    Returns:
        mixer running: bool
    """
    @property
    def mixing(self) -> bool:
        """
        bool: True if the mixer is running (automatic mode).
        """
        return self.read("aut_mixer")

    """Checks if the mixingpump is running
    Returns:
        mixingpump is running: bool
    """
    @property
    def pumping(self) -> bool:
        """
        bool: True if the mixingpump is running.
        """
        return self.pumping_net or self.pumping_fc

    """Checks if the mixingpump is running on power supply (in automatic mode)
    Returns:
        mixingpump is running on power supply: bool
    """
    @property
    def pumping_net(self) -> bool:
        """
        bool: True if the mixingpump is running on power supply (automatic mode).
        """
        return self.read("aut_mixingpump_net")

    """Checks if the mixingpump is running on frequency converter supply (in automatic mode)
    Returns:
        mixingpump is running on frequency converter supply: bool
    """
    @property
    def pumping_fc(self) -> bool:
        """
        bool: True if the mixingpump is running on frequency converter supply (automatic mode).
        """
        return self.read("aut_mixingpump_fc")

    """Checks if the selenoid valve is open (in automatic mode)
    Returns:
        selenoid valve is open: bool
    """
    @property
    def solenoidvalve(self) -> bool:
        """
        bool: True if the solenoid valve is open (automatic mode).
        """
        return self.read("aut_solenoid_valve")
    
    """Checks if the water pump is running (in automatic mode)
    Returns:
        waterpump is running: bool
    """
    @property
    def waterpump(self) -> bool:
        """
        bool: True if the water pump is running (automatic mode).
        """
        return self.read("aut_waterpump")

    """Checks if remote is connected
    Returns:
        remote is connected: bool
    """
    @property
    def remote(self) -> bool:
        """
        bool: True if remote is connected.
        """
        return self.read("Remote_connected")



    def setDigital(self, pin: int, value: bool):
        """
        Changes the state of a digital output.

        Args:
            pin (int): Pin number.
            value (bool): True for high, False for low.

        Raises:
            ValueError: If pin is out of range.
        """
        try:
            self.change(f"reserve_DO_{pin}", value, "bool")
        except KeyError:
            raise ValueError(f"Pin number ({pin}) out of range")
        
    def getDigital(self, pin: int) -> bool:
        """
        Reads the state of a digital input.

        Args:
            pin (int): Pin number.

        Returns:
            bool: True for high, False for low.

        Raises:
            ValueError: If pin is out of range.
        """
        try:
            return self.read(f"reserve_DI_{pin}")
        except KeyError:
            raise ValueError(f"Pin number ({pin}) out of range")
        
    def setAnalog(self, pin: int, value: int):
        """
        Changes the state of an analog output.

        Args:
            pin (int): Pin number.
            value (int): Value to set (0 to 65535).

        Raises:
            ValueError: If pin is out of range.
        """
        try:
            self.change(f"reserve_AO_{pin}", value, "uint16")
        except KeyError:
            raise ValueError(f"Pin number ({pin}) out of range")
        
    def getAnalog(self, pin: int) -> int:
        """
        Reads the state of an analog input.

        Args:
            pin (int): Pin number (1 - 5).

        Returns:
            int: Actual value (0 - 65535).

        Raises:
            ValueError: If pin is out of range.
        """
        try:
            return self.read(f"reserve_AI_{pin}")
        except KeyError:
            raise ValueError(f"Pin number ({pin}) out of range")
    


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