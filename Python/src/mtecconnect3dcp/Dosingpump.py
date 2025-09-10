from .Machine import Machine

class Dosingpump(Machine):
    """
    Class for controlling a dosing pump via OPC-UA.
    Inherits from Machine.
    """
    @property
    def running(self) -> bool:
        """
        bool: True if the dosingpump is running, False otherwise.
        """
        return self.read("state_dosingpump_on")
    @running.setter
    def running(self, state: bool):
        """
        Set the running state of the dosingpump.

        Args:
            state (bool): True to start, False to stop.
        """
        self.change("state_dosingpump_on", state, "bool")

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
    def real_speed(self) -> int:
        """
        int: Real speed of the dosingpump in ml/min.
        """
        return self.read("actual_value_additive")

    @property
    def real_pressure(self) -> float:
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
    def error(self) -> bool:
        """
        bool: True if the dosingpump is in error state.
        """
        return self.read("error_dosingpump")

    @property
    def error_no(self) -> int:
        """
        int: Error number of the dosingpump (0 = none).
        """
        return self.read("error_no_dosingpump")

    @property
    def ready(self) -> bool:
        """
        bool: True if the dosingpump is ready for operation.
        """
        return self.read("Ready_for_operation_dosingpump")