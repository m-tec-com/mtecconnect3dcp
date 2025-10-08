from .OPCUAMachine import SubscriptionWrapper
from .Mixingpump import Mixingpump

class Smp(Mixingpump):
    """
    SMP

    OPC-UA client class for m-tec SMP machines (Mixingpump).
    Inherits from Mixingpump.
    """
    
    @property
    def s_rotaryvalve(self) -> bool:
        """
        bool: True if the rotary valve is running in automatic mode.
        """
        return self.safe_read("aut_cw", False)

    @s_rotaryvalve.setter
    def s_rotaryvalve(self, callback: callable):
        """
        Create a subscription for the rotary valve state (automatic mode).

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("aut_cw", callback)
    
    @property
    def s_compressor(self) -> bool:
        """
        bool: True if the compressor is running in automatic mode.
        """
        return self.safe_read("aut_comp", False)

    @s_compressor.setter
    def s_compressor(self, callback: callable):
        """
        Create a subscription for the compressor state (automatic mode).

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("aut_comp", callback)
    
    @property
    def s_vibrator_1(self) -> bool:
        """
        bool: True if vibrator 1 is running in automatic mode.
        """
        return self.safe_read("aut_vib_1", False)

    @s_vibrator_1.setter
    def s_vibrator_1(self, callback: callable):
        """
        Create a subscription for the vibrator 1 state (automatic mode).

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("aut_vib_1", callback)
    
    @property
    def s_vibrator_2(self) -> bool:
        """
        bool: True if vibrator 2 is running in automatic mode.
        """
        return self.safe_read("aut_vib_2", False)
    
    @s_vibrator_2.setter
    def s_vibrator_2(self, callback: callable):
        """
        Create a subscription for the vibrator 2 state (automatic mode).

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("aut_vib_2", callback)
    
    @property
    def m_silolevel(self) -> float:
        """
        float: Silo level in percentage (0-100%).
        """
        return self.safe_read("Silo_Level", 0.0)

    @m_silolevel.setter
    def m_silolevel(self, callback: callable):
        """
        Create a subscription for the silo level in percentage.

        Args:
            callback (callable): Callback function (optional parameters: 'value', 'parameter' and 'subscription').
        """
        if not callable(callback):
            raise ValueError("Callback is not callable.")
        self.easy_subscribe("Silo_Level", callback)