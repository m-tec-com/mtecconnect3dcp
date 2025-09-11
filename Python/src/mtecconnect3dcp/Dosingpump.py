from .OPCUAMachine import OPCUAMachine

class Dosingpump(OPCUAMachine):
    """
    Class for controlling a dosing pump via OPC-UA.
    Inherits from OPCUAMachine.
    """
    @property
    def run(self) -> bool:
        """
        bool: True if the dosingpump is set to run, False otherwise.
        """
        return self.read("state_dosingpump_on")
    @run.setter
    def run(self, state: bool):
        """
        Set the running state of the dosingpump.

        Args:
            state (bool): True to start, False to stop.
        """
        self.change("state_dosingpump_on", state, "bool")

    @property
    def s_running(self) -> bool:
        """
        bool: True if the dosingpump is running, False otherwise.
        """
        return self.read("state_fc_dosingpump")

    @property
    def speed(self) -> float:
        """
        float: Speed setting of the dosingpump in ml/min.
        """
        return self.read("set_value_dosingpump")
    @speed.setter
    def speed(self, speed: float):
        """
        Set the speed of the dosingpump.

        Args:
            speed (float): Speed in ml/min.
        """
        self.change("set_value_dosingpump", float(speed), "float")

    @property
    def m_speed(self) -> int:
        """
        int: Real speed of the dosingpump in ml/min.
        """
        return self.read("actual_value_additive")

    @property
    def m_dosingspeed(self) -> float:
        """
        float: Real speed of the dosingpump in %.
        """
        return self.read("actual_value_dosingpump")

    @property
    def m_pressure(self) -> float:
        """
        float: Real pressure of the dosingpump in bar.
        """
        return self.read("actual_value_pressure_dosingpump")

    @property
    def cleaning(self) -> bool:
        """
        bool: True if cleaning water is running, False otherwise.
        """
        return self.read("state_solenoid_valve")
    @cleaning.setter
    def cleaning(self, state: bool):
        """
        Set the cleaning water state.

        Args:
            state (bool): True to start, False to stop.
        """
        self.change("state_solenoid_valve", state, "bool")

    @property
    def s_error(self) -> bool:
        """
        bool: True if the dosingpump is in error state.
        """
        return self.read("error_dosingpump")

    @property
    def s_error_no(self) -> int:
        """
        int: Error number of the dosingpump (0 = none).
        """
        return self.read("error_no_dosingpump")

    @property
    def s_ready(self) -> bool:
        """
        bool: True if the dosingpump is ready for operation.
        """
        return self.read("Ready_for_operation_dosingpump")
    
    @property
    def s_emergency_stop(self) -> bool:
        """
        bool: True if emergency stop is ok, False otherwise.
        """
        return bool(self.safe_read("emergency_stop_ok", False))

    @property
    def s_on(self) -> bool:
        """
        bool: True if the machine is powered on, False otherwise.
        """
        return bool(self.safe_read("state_machine_on", False))
    
    @property
    def s_remote(self) -> bool:
        """
        bool: True if remote is connected.
        """
        return self.read("Remote_connected_dosingpump")
    
    @property
    def s_fc(self) -> bool:
        """
        bool: True if frequency converter is ok, False otherwise.
        """
        return not bool(self.safe_read("state_fc_error_dosingpump", True)) # Inverted
    
    @property
    def s_operating_pressure(self) -> bool:
        """
        bool: True if operating pressure is ok, False otherwise.
        """
        return not bool(self.safe_read("state_pressure_error_dosingpump", True)) # Inverted