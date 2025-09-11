from .OPCUAMachine import OPCUAMachine, SubscriptionWrapper

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

    @s_running.setter
    def s_running(self, callback: callable):
        """
        Create a subscription for the running state of the dosingpump.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_fc_dosingpump", callback)

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
        self.change("set_value_dosingpump", speed, "float")

    @property
    def m_speed(self) -> int:
        """
        int: Real speed of the dosingpump in ml/min.
        """
        return self.read("actual_value_additive")

    @m_speed.setter
    def m_speed(self, callback: callable):
        """
        Create a subscription for the real speed of the dosingpump in ml/min.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_additive", callback)

    @property
    def m_dosingspeed(self) -> float:
        """
        float: Real speed of the dosingpump in %.
        """
        return self.read("actual_value_dosingpump")

    @m_dosingspeed.setter
    def m_dosingspeed(self, callback: callable):
        """
        Create a subscription for the real speed of the dosingpump in %.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_dosingpump", callback)

    @property
    def m_pressure(self) -> float:
        """
        float: Real pressure of the dosingpump in bar.
        """
        return self.read("actual_value_pressure_dosingpump")

    @m_pressure.setter
    def m_pressure(self, callback: callable):
        """
        Create a subscription for the real pressure of the dosingpump in bar.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_pressure_dosingpump", callback)

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

    @s_error.setter
    def s_error(self, callback: callable):
        """
        Create a subscription for the error state of the dosingpump.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("error_dosingpump", callback)

    @property
    def s_error_no(self) -> int:
        """
        int: Error number of the dosingpump (0 = none).
        """
        return self.read("error_no_dosingpump")

    @s_error_no.setter
    def s_error_no(self, callback: callable):
        """
        Create a subscription for the error number of the dosingpump.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("error_no_dosingpump", callback)

    @property
    def s_ready(self) -> bool:
        """
        bool: True if the dosingpump is ready for operation.
        """
        return self.read("Ready_for_operation_dosingpump")

    @s_ready.setter
    def s_ready(self, callback: callable):
        """
        Create a subscription for the ready state of the dosingpump.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("Ready_for_operation_dosingpump", callback)
    
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
            callback (callable): Callback function.
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
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_machine_on", callback)
    
    @property
    def s_remote(self) -> bool:
        """
        bool: True if remote is connected.
        """
        return self.read("Remote_connected_dosingpump")

    @s_remote.setter
    def s_remote(self, callback: callable):
        """
        Create a subscription for the remote connection state.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("Remote_connected_dosingpump", callback)
    
    @property
    def s_fc(self) -> bool:
        """
        bool: True if frequency converter is ok, False otherwise.
        """
        return not bool(self.safe_read("state_fc_error_dosingpump", True)) # Inverted

    @s_fc.setter
    def s_fc(self, callback: callable):
        """
        Create a subscription for the frequency converter state.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback)
            sw.trigger(value=not value, parameter=parameter)
        self.easy_subscribe("state_fc_error_dosingpump", cb, False)
    
    @property
    def s_operating_pressure(self) -> bool:
        """
        bool: True if operating pressure is ok, False otherwise.
        """
        return not bool(self.safe_read("state_pressure_error_dosingpump", True)) # Inverted

    @s_operating_pressure.setter
    def s_operating_pressure(self, callback: callable):
        """
        Create a subscription for the operating pressure state.

        Args:
            callback (callable): Callback function.
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback)
            sw.trigger(value=not value, parameter=parameter)
        self.easy_subscribe("state_pressure_error_dosingpump", cb, False)