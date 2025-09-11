from .OPCUAMachine import OPCUAMachine

class Mixingpump(OPCUAMachine):
    """
    Class for controlling a mixing pump via OPC-UA.
    Inherits from OPCUAMachine.
    """
    @property
    def run(self) -> bool:
        """
        bool: True if the machine is running, False otherwise.
        """
        return bool(self.read("Remote_start"))
    @run.setter
    def run(self, state: bool):
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
    def m_speed(self) -> float:
        """
        float: Real speed of the mixingpump in Hz.
        """
        speed = self.read("actual_value_mixingpump")
        return speed * 50 / 65535 # 50Hz = 65535, 0Hz = 0

    @property
    def s_error(self) -> bool:
        """
        bool: True if the machine is in error state.
        """
        return self.read("error")
    
    @property
    def s_error_no(self) -> int:
        """
        int: Error number of the machine (0 = none).
        """
        return self.read("error_no")

    @property
    def s_ready(self) -> bool:
        """
        bool: True if the machine is ready for operation.
        """
        return self.read("Ready_for_operation")

    @property
    def s_mixing(self) -> bool:
        """
        bool: True if the mixer is running (automatic mode).
        """
        return self.read("aut_mixer")

    @property
    def s_pumping(self) -> bool:
        """
        bool: True if the mixingpump is running.
        """
        return self.s_pumping_net or self.s_pumping_fc

    @property
    def s_pumping_net(self) -> bool:
        """
        bool: True if the mixingpump is running on power supply (automatic mode).
        """
        return self.read("aut_mixingpump_net")

    @property
    def s_pumping_fc(self) -> bool:
        """
        bool: True if the mixingpump is running on frequency converter supply (automatic mode).
        """
        return self.read("aut_mixingpump_fc")

    @property
    def s_solenoidvalve(self) -> bool:
        """
        bool: True if the solenoid valve is open (automatic mode).
        """
        return self.read("aut_solenoid_valve")
    
    @property
    def s_waterpump(self) -> bool:
        """
        bool: True if the water pump is running (automatic mode).
        """
        return self.read("aut_waterpump")

    @property
    def s_remote(self) -> bool:
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
            pin (int): Pin number.

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
        """
        DEPRECATED: Use '.run = True' instead.
        """
        self.run = True
    def stop(self):
        """
        DEPRECATED: Use '.run = False' instead.
        """
        self.run = False
    def setSpeed(self, speed):
        """
        DEPRECATED: Use '.speed = speed' (20-50Hz instead of 0-100%) instead.
        """
        self.speed = speed * 30 / 100 + 20 # 100% = 50Hz, 0% = 20Hz
    def getSpeed(self):
        """
        DEPRECATED: Use '.speed' (20-50Hz instead of 0-100%) instead.
        """
        return self.m_speed
    def isError(self):
        """
        DEPRECATED: Use '.error' instead.
        """
        return self.s_error
    def getError(self):
        """
        DEPRECATED: Use '.error_no' instead.
        """
        return self.s_error_no
    def isReadyForOperation(self):
        """
        DEPRECATED: Use '.ready' instead.
        """
        return self.ready
    def isMixerRunning(self):
        """
        DEPRECATED: Use '.s_mixing' instead.
        """
        return self.s_mixing
    def isMixingpumpRunningNet(self):
        """
        DEPRECATED: Use '.s_pumping_net' instead.
        """
        return self.s_pumping_net
    def isMixingpumpRunningFc(self):
        """
        DEPRECATED: Use '.s_pumping_fc' instead.
        """
        return self.s_pumping_fc
    def isMixingpumpRunning(self):
        """
        DEPRECATED: Use '.s_pumping' instead.
        """
        return self.s_pumping
    def isSolenoidValve(self):
        """
        DEPRECATED: Use '.s_solenoidvalve' instead.
        """
        return self.s_solenoidvalve
    def isWaterpump(self):
        """
        DEPRECATED: Use '.s_waterpump' instead.
        """
        return self.s_waterpump
    def isRemote(self):
        """
        DEPRECATED: Use '.s_remote' instead.
        """
        return self.s_remote