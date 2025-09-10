from .Machine import Machine

class Printhead(Machine):
    """
    Class for controlling a printhead via OPC-UA.
    Inherits from Machine.
    """
    @property
    def running(self) -> bool:
        """
        bool: True if the printhead is running, False otherwise.
        """
        return self.read("state_printhead_on")
    @running.setter
    def running(self, state: bool):
        """
        Set the running state of the printhead.

        Args:
            state (bool): True to start, False to stop.
        """
        self.change("state_printhead_on", state, "bool")

    @property
    def speed(self) -> float:
        """
        float: Speed setting of the printhead in 1/min.
        """
        return self.read("set_value_printhead")
    @speed.setter
    def speed(self, speed: float):
        """
        Set the speed of the printhead.

        Args:
            speed (float): Speed in 1/min.
        """
        self.change("set_value_printhead", float(speed), "float")

    @property
    def real_speed(self) -> int:
        """
        int: Real speed of the printhead in 1/min.
        """
        return self.read("actual_value_printhead")

    @property
    def real_pressure(self) -> float:
        """
        float: Real pressure of the printhead in bar (if sensor installed).
        """
        return self.read("actual_value_pressure_printhead")

    @property
    def error(self) -> bool:
        """
        bool: True if the printhead is in error state.
        """
        return self.read("error_printhead")

    @property
    def error_no(self) -> int:
        """
        int: Error number of the printhead (0 = none).
        """
        return self.read("error_no_printhead")

    @property
    def ready(self) -> bool:
        """
        bool: True if the printhead is ready for operation.
        """
        return self.read("Ready_for_operation_printhead")