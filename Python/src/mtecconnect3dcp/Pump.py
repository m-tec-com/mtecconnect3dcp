from .ModbusMachine import ModbusMachine

class Pump(ModbusMachine):
    """
    Class for controlling a pump via Modbus.
    Inherits from ModbusMachine.
    """
    # Class-level bit masks for status decoding
    _RUNNING_MASK = 0x0400
    _REVERSE_MASK = 0x0200

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._last_speed: float = 0.0
        self._last_running: bool = False
        self._last_reverse: bool = False

    @property
    def s_ready(self) -> bool:
        """
        bool: True if the machine is ready for operation (on, remote, mixer and mixingpump on).
        """
        switches = self.read("FD06")
        return ((switches % 32) - (switches % 16) != 0)

    @property
    def run(self) -> bool:
        """
        bool: True if the pump is set to run, False otherwise.
        """
        return (self.read("FA00") & self._RUNNING_MASK) != 0

    @run.setter
    def run(self, state: bool):
        """
        Set the running state of the pump.

        Args:
            state (bool): True to start, False to stop.
        """
        self._last_running = state
        if state:
            if self._last_reverse:
                v = self.write("FA00", 0xC600)
            else:
                v = self.write("FA00", 0xC400)
            self.keepalive()
            return v
        else:
            v = self.write("FA00", 0x0000)
            self.stop_keepalive()
            return v
    
    @property
    def s_pumping(self) -> bool:
        """
        bool: True if the pump is running, False otherwise.
        """
        return abs(self.m_speed) > 0
    
    @property
    def s_pumping_forward(self) -> bool:
        """
        bool: True if the pump is running forward, False otherwise.
        """
        return self.m_speed > 0
    
    @property
    def s_pumping_reverse(self) -> bool:
        """
        bool: True if the pump is running in reverse, False otherwise.
        """
        return self.m_speed < 0

    @property
    def reverse(self) -> bool:
        """
        bool: True if the pump is running in reverse, False otherwise.
        """
        return (self.read("FA00") & self._REVERSE_MASK) != 0

    @reverse.setter
    def reverse(self, state: bool):
        """
        Set the running direction of the pump.

        Args:
            state (bool): True for reverse, False for forward.
        """
        self._last_reverse = state
        if self._last_running:
            if state:
                return self.write("FA00", 0xC600)
            else:
                return self.write("FA00", 0xC400)
        else:
            return self.write("FA00", 0x0000)

    @property
    def _frequency(self) -> float:
        """
        float: Frequency of the pump in Hz.
        """
        return self.read("FD00") / 100

    @_frequency.setter
    def _frequency(self, value: float):
        """
        Set the frequency of the pump.

        Args:
            value (float): Frequency in Hz.
        """
        return self.write("FA01", int(value * 100))

    @property
    def m_voltage(self) -> float:
        """
        float: Voltage of the pump in V.
        """
        return self.read("FD05") / 100

    @property
    def m_current(self) -> float:
        """
        float: Current of the pump in A.
        """
        return self.read("FD03") / 100

    @property
    def m_torque(self) -> float:
        """
        float: Torque of the pump in Nm.
        """
        return self.read("FD18") / 100

    def emergency_stop(self):
        """
        Emergency stop for the pump.
        """
        return self.write("FA00", 0x1000)

    @property
    def m_speed(self) -> float:
        """
        float: Real speed of the pump in Hz. Negative values indicate reverse direction.
        """
        if self.reverse:
            return -self._frequency
        return self._frequency

    @property
    def speed(self) -> float:
        """
        float: Set speed of the pump. Negative values indicate reverse direction.
        """
        return self._last_speed

    @speed.setter
    def speed(self, value: float):
        """
        Set the speed of the pump.

        Args:
            value (float): Speed. Negative values indicate reverse direction.
        """
        if value == self._last_speed:
            return
        if value == 0:
            self.run = False
        else:
            if value < 0 and not self._last_speed < 0:
                self.reverse = True
            elif value > 0 and not self._last_speed > 0:
                self.reverse = False
            self._frequency = abs(value)
        self._last_speed = value


    """Backward compatibility"""
    def start(self):
        """
        DEPRECATED: Use '.run = True' instead.
        """
        self.reverse = False
        self.run = True
    def start_reverse(self):
        """
        DEPRECATED: Use '.reverse = True' and '.run = True' instead.
        """
        self.reverse = True
        self.run = True
    def stop(self):
        """
        DEPRECATED: Use '.run = False' instead.
        """
        self.run = False