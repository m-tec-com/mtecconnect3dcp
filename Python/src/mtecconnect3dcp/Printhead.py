from .OPCUAMachine import OPCUAMachine, SubscriptionWrapper

class Printhead(OPCUAMachine):
    """
    Class for controlling a printhead via OPC-UA.
    Inherits from OPCUAMachine.
    """
    @property
    def run(self) -> bool:
        """
        bool: True if the printhead is set to run, False otherwise.
        """
        return self.read("state_printhead_on")

    @run.setter
    def run(self, state: bool):
        """
        Set the running state of the printhead.

        Args:
            state (bool): True to start, False to stop.
        """
        self.change("state_printhead_on", state, "bool")

    @property
    def s_running(self) -> bool:
        """
        bool: True if the printhead is running, False otherwise.
        """
        return self.read("state_fc_printhead")

    @s_running.setter
    def s_running(self, callback: callable):
        """
        Create a subscription for the running state of the printhead.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_fc_printhead", callback)

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
        self.change("set_value_printhead", speed, "float")

    @property
    def m_speed(self) -> int:
        """
        int: Real speed of the printhead in 1/min.
        """
        return self.read("actual_value_printhead")

    @m_speed.setter
    def m_speed(self, callback: callable):
        """
        Create a subscription for the real speed of the printhead in 1/min.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_printhead", callback)

    @property
    def m_pressure(self) -> float:
        """
        float: Real pressure of the printhead in bar (if sensor installed).
        """
        return self.read("actual_value_pressure_printhead")

    @m_pressure.setter
    def m_pressure(self, callback: callable):
        """
        Create a subscription for the real pressure of the printhead in bar.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_pressure_printhead", callback)

    @property
    def s_error(self) -> bool:
        """
        bool: True if the printhead is in error state.
        """
        return self.read("error_printhead")

    @s_error.setter
    def s_error(self, callback: callable):
        """
        Create a subscription for the error state of the printhead.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("error_printhead", callback)

    @property
    def s_error_no(self) -> int:
        """
        int: Error number of the printhead (0 = none).
        """
        return self.read("error_no_printhead")

    @s_error_no.setter
    def s_error_no(self, callback: callable):
        """
        Create a subscription for the error number of the printhead.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("error_no_printhead", callback)

    @property
    def s_ready(self) -> bool:
        """
        bool: True if the printhead is ready for operation.
        """
        return self.read("Ready_for_operation_printhead")

    @s_ready.setter
    def s_ready(self, callback: callable):
        """
        Create a subscription for the ready state of the printhead.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("Ready_for_operation_printhead", callback)
    
    @property
    def s_emergency_stop(self) -> bool:
        """
        bool: True if emergency stop is ok, False otherwise.
        """
        return bool(self.safe_read("emergency_stop_ok", False))

    @s_emergency_stop.setter
    def s_emergency_stop(self, callback: callable):
        """
        Create a subscription for the emergency stop state.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("emergency_stop_ok", callback)

    @property
    def s_on(self) -> bool:
        """
        bool: True if the machine is powered on, False otherwise.
        """
        return bool(self.safe_read("state_machine_on", False))

    @s_on.setter
    def s_on(self, callback: callable):
        """
        Create a subscription for the machine power state.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_machine_on", callback)
    
    @property
    def s_remote(self) -> bool:
        """
        bool: True if remote is connected.
        """
        return self.read("Remote_connected_printhead")

    @s_remote.setter
    def s_remote(self, callback: callable):
        """
        Create a subscription for the remote connection state.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("Remote_connected_printhead", callback)
    
    @property
    def s_fc(self) -> bool:
        """
        bool: True if frequency converter is ok, False otherwise.
        """
        return not bool(self.safe_read("state_fc_error_printhead", True)) # Inverted

    @s_fc.setter
    def s_fc(self, callback: callable):
        """
        Create a subscription for the frequency converter state.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback, subscription)
            sw.trigger(value=not value, parameter=parameter)
        subscription = self.easy_subscribe("state_fc_error_printhead", cb, False)

    @property
    def s_operating_pressure(self) -> bool:
        """
        bool: True if operating pressure is ok, False otherwise.
        """
        return not bool(self.safe_read("state_pressure_error_printhead", True)) # Inverted

    @s_operating_pressure.setter
    def s_operating_pressure(self, callback: callable):
        """
        Create a subscription for the operating pressure state.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback, subscription)
            sw.trigger(value=not value, parameter=parameter)
        subscription = self.easy_subscribe("state_pressure_error_printhead", cb, False)