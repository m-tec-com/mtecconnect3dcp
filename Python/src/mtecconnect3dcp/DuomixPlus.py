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
        self.safe_change("set_value_dosingpump", float(speed), "float")

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

    @property
    def real_water(self) -> float:
        """
        float: Real amount of water in l/h.
        """
        return float(self.safe_read("actual_value_water_flow", 0.0))
    
    @property
    def real_water_temperature(self) -> float:
        """
        float: Real temperature of the water in °C.
        """
        return float(self.safe_read("actual_value_water_temp", 0.0))

    @property
    def real_temperature(self) -> float:
        """
        float: Real temperature of the mortar in °C.
        """
        return float(self.safe_read("actual_value_mat_temp", 0.0))

    @property
    def real_pressure(self) -> float:
        """
        float: Real pressure of the mortar in bar.
        """
        return float(self.safe_read("actual_value_pressure", 0.0))
    
    @property
    def emergency_stop(self) -> bool:
        """
        bool: True if emergency stop is ok, False otherwise.
        """
        return bool(self.safe_read("emergency_stop_ok", False))

    @property
    def on(self) -> bool:
        """
        bool: True if the machine is powered on, False otherwise.
        """
        return bool(self.safe_read("state_machine_on", False))
    
    @property
    def safety(self) -> tuple:
        """
        tuple: (bool, bool) Tuple with (mixingpump, mixer), true if ok.
        """
        return (bool(self.safe_read("state_safety_mp", False)), bool(self.safe_read("state_safety_mixer", False)))

    @property
    def circuitbreaker(self) -> tuple:
        """
        tuple: (bool, bool) Tuple with (fc, other). True if the circuit breaker is not tripped
        """
        return (bool(self.safe_read("state_circuit_breaker_fc_ok", False)), bool(self.safe_read("state_circuit_breaker_ok", False)))
    
    @property
    def fc(self) -> bool:
        """
        bool: True if frequency converter is ok, False otherwise.
        """
        return not bool(self.safe_read("state_fc_error", True)) # Inverted
    
    @property
    def water_pressure(self) -> bool:
        """
        bool: True if water pressure is ok, False otherwise.
        """
        return bool(self.safe_read("state_water_pressure_ok", False))
    
    @property
    def hopper_wet(self) -> bool:
        """
        bool: True if pumping hopper level is ok, False otherwise.
        """
        return bool(self.safe_read("state_wetmaterialprobe", False))
    
    @property
    def hopper_dry(self) -> bool:
        """
        bool: True if dry material hopper level is ok, False otherwise.
        """
        return not bool(self.safe_read("state_drymaterialprobe", True)) # Inverted
    
    @property
    def running_local(self) -> bool:
        """
        bool: True if the machine is running in local mode
        """
        return not bool(self.safe_read("state_remote_start_local", True))
    
    @property
    def phase_reversed(self) -> bool:
        """
        bool: True if the phase is reversed, False otherwise.
        """
        return bool(self.safe_read("state_relay_rotary_switch", False))

    @property
    def running_forward(self) -> bool:
        """
        bool: True if the mixingpump is running forward.
        """
        return bool(self.safe_read("state_fc_fwd", False))
    
    @property
    def running_reverse(self) -> bool:
        """
        bool: True if the mixingpump is running in reverse.
        """
        return bool(self.safe_read("state_fc_rwd", False))
    
    @property
    def valve(self) -> float:
        """
        float: Valve position in %.
        """
        return float(self.safe_read("actual_value_water_valve", 0.0))




    """Backward compatibility"""
    def startDosingpump(self):
        self.dosingpump = True
    def stopDosingpump(self):
        self.dosingpump = False
    def setSpeedDosingpump(self, speed):
        self.dosingspeed = speed
    def setWater(self, speed):
        self.water = speed