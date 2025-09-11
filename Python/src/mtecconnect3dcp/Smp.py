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
    
    @property
    def s_compressor(self) -> bool:
        """
        bool: True if the compressor is running in automatic mode.
        """
        return self.safe_read("aut_comp", False)
    
    @property
    def s_vibrator(self) -> tuple:
        """
        tuple: (vibrator1, vibrator2) True if the vibrators are running in automatic mode.
        """
        return (self.safe_read("aut_vib_1", False), self.safe_read("aut_vib_2", False))
    
    @property
    def m_silolevel(self) -> float:
        """
        float: Silo level in percentage (0-100%).
        """
        return self.safe_read("Silo_Level", 0.0)