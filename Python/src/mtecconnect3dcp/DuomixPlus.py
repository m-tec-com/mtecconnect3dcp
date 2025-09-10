from .Mixingpump import Mixingpump

class DuomixPlus (Mixingpump):
    """
    DuomixPlus

    OPC-UA client class for m-tec Duo-Mix 3DCP+ machines (Mixingpump).
    Inherits from Mixingpump.
    """
    
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