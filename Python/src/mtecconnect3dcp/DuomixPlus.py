from .OPCUAMachine import SubscriptionWrapper
from .Mixingpump import Mixingpump

class DuomixPlus (Mixingpump):
    """
    DuomixPlus

    OPC-UA client class for m-tec Duo-Mix 3DCP+ machines (Mixingpump).
    Inherits from Mixingpump.
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
        self.safe_change("set_value_dosingpump", speed, "float")

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
        self.safe_change("set_value_water_flow", speed, "float")

    @property
    def m_water(self) -> float:
        """
        float: Real amount of water in l/h.
        """
        return float(self.safe_read("actual_value_water_flow", 0.0))
    @m_water.setter
    def m_water(self, callback: callable):
        """
        Create a subscription for the real amount of water in l/h.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_water_flow", callback)

    @property
    def m_water_temperature(self) -> float:
        """
        float: Real temperature of the water in °C.
        """
        return float(self.safe_read("actual_value_water_temp", 0.0))

    @m_water_temperature.setter
    def m_water_temperature(self, callback: callable):
        """
        Create a subscription for the real temperature of the water in °C.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_water_temp", callback)

    @property
    def m_temperature(self) -> float:
        """
        float: Real temperature of the mortar in °C.
        """
        return float(self.safe_read("actual_value_mat_temp", 0.0))

    @m_temperature.setter
    def m_temperature(self, callback: callable):
        """
        Create a subscription for the real temperature of the mortar in °C.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_mat_temp", callback)

    @property
    def m_pressure(self) -> float:
        """
        float: Real pressure of the mortar in bar.
        """
        return float(self.safe_read("actual_value_pressure", 0.0))

    @m_pressure.setter
    def m_pressure(self, callback: callable):
        """
        Create a subscription for the real pressure of the mortar in bar.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_pressure", callback)
    
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
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
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
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_machine_on", callback)
    
    @property
    def s_safety_mp(self) -> bool:
        """
        bool: True if the safety (mixingpump) is ok, False otherwise.
        """
        return bool(self.safe_read("state_safety_mp", False))

    @s_safety_mp.setter
    def s_safety_mp(self, callback: callable):
        """
        Create a subscription for the safety (mixingpump).

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_safety_mp", callback)

    @property
    def s_safety_mixer(self) -> bool:
        """
        bool: True if the safety (mixer) is ok, False otherwise.
        """
        return bool(self.safe_read("state_safety_mixer", False))

    @s_safety_mixer.setter
    def s_safety_mixer(self, callback: callable):
        """
        Create a subscription for the safety (mixer).

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_safety_mixer", callback)

    @property
    def s_circuitbreaker(self) -> bool:
        """
        bool: True if circuit breaker is not tripped, False otherwise.
        """
        return bool(self.safe_read("state_circuit_breaker_ok", False))
       

    @property
    def s_circuitbreaker_fc(self) -> bool:
        """
        bool: True if frequency converter circuit breaker is not tripped, False otherwise.
        """
        return bool(self.safe_read("state_circuit_breaker_fc_ok", False))

    @s_circuitbreaker.setter
    def s_circuitbreaker(self, callback: callable):
        """
        Create a subscription for the circuit breaker state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_circuit_breaker_ok", callback)

    @s_circuitbreaker_fc.setter
    def s_circuitbreaker_fc(self, callback: callable):
        """
        Create a subscription for the frequency converter circuit breaker state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_circuit_breaker_fc_ok", callback)
    
    @property
    def s_fc(self) -> bool:
        """
        bool: True if frequency converter is ok, False otherwise.
        """
        return not bool(self.safe_read("state_fc_error", True)) # Inverted

    @s_fc.setter
    def s_fc(self, callback: callable):
        """
        Create a subscription for the frequency converter state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback)
            sw.trigger(value=not value, parameter=parameter)
        self.easy_subscribe("state_fc_error", cb, False)

    @property
    def s_water_pressure(self) -> bool:
        """
        bool: True if water pressure is ok, False otherwise.
        """
        return bool(self.safe_read("state_water_pressure_ok", False))

    @s_water_pressure.setter
    def s_water_pressure(self, callback: callable):
        """
        Create a subscription for the water pressure state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_water_pressure_ok", callback)
    
    @property
    def s_hopper_wet(self) -> bool:
        """
        bool: True if pumping hopper level is ok, False otherwise.
        """
        return bool(self.safe_read("state_wetmaterialprobe", False))

    @s_hopper_wet.setter
    def s_hopper_wet(self, callback: callable):
        """
        Create a subscription for the wet hopper level state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_wetmaterialprobe", callback)
    
    @property
    def s_hopper_dry(self) -> bool:
        """
        bool: True if dry material hopper level is ok, False otherwise.
        """
        return not bool(self.safe_read("state_drymaterialprobe", True)) # Inverted

    @s_hopper_dry.setter
    def s_hopper_dry(self, callback: callable):
        """
        Create a subscription for the dry hopper level state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback)
            sw.trigger(value=not value, parameter=parameter)
        self.easy_subscribe("state_drymaterialprobe", cb, False)
    
    @property
    def s_running_local(self) -> bool:
        """
        bool: True if the machine is running in local mode
        """
        return not bool(self.safe_read("state_remote_start_local", True))

    @s_running_local.setter
    def s_running_local(self, callback: callable):
        """
        Create a subscription for the local running state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        def cb(value, parameter):
            sw = SubscriptionWrapper(callback)
            sw.trigger(value=not value, parameter=parameter)
        self.easy_subscribe("state_remote_start_local", cb, False)
    
    @property
    def s_phase_reversed(self) -> bool:
        """
        bool: True if the phase is reversed, False otherwise.
        """
        return bool(self.safe_read("state_relay_rotary_switch", False))

    @s_phase_reversed.setter
    def s_phase_reversed(self, callback: callable):
        """
        Create a subscription for the phase reversed state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_relay_rotary_switch", callback)

    @property
    def s_running_forward(self) -> bool:
        """
        bool: True if the mixingpump is running forward.
        """
        return bool(self.safe_read("state_fc_fwd", False))

    @s_running_forward.setter
    def s_running_forward(self, callback: callable):
        """
        Create a subscription for the forward running state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_fc_fwd", callback)
    
    @property
    def s_running_reverse(self) -> bool:
        """
        bool: True if the mixingpump is running in reverse.
        """
        return bool(self.safe_read("state_fc_rwd", False))

    @s_running_reverse.setter
    def s_running_reverse(self, callback: callable):
        """
        Create a subscription for the reverse running state.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("state_fc_rwd", callback)
    
    @property
    def m_valve(self) -> float:
        """
        float: Valve position in %.
        """
        return float(self.safe_read("actual_value_water_valve", 0.0))

    @m_valve.setter
    def m_valve(self, callback: callable):
        """
        Create a subscription for the valve position.

        Args:
            callback (callable): Callback function (optional parameters: 'value' and 'parameter').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("actual_value_water_valve", callback)




    """Backward compatibility"""
    def startDosingpump(self):
        """
        DEPRECATED. Use '.dosingpump = True' instead.
        """
        self.dosingpump = True
    def stopDosingpump(self):
        """
        DEPRECATED. Use '.dosingpump = False' instead.
        """
        self.dosingpump = False
    def setSpeedDosingpump(self, speed):
        """
        DEPRECATED. Use '.dosingspeed = speed' instead.
        """
        self.dosingspeed = speed
    def setWater(self, speed):
        """
        DEPRECATED. Use '.water = speed' instead.
        """
        self.water = speed