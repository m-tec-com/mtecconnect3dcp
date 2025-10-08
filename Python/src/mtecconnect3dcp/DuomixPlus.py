from .OPCUAMachine import SubscriptionWrapper
from .Duomix import Duomix
from .MixingpumpPlus import MixingpumpPlus

class DuomixPlus (Duomix, MixingpumpPlus):
    """
    DuomixPlus

    OPC-UA client class for m-tec Duo-Mix 3DCP+ machines (Mixingpump).
    Inherits from Duomix and MixingpumpPlus.
    """

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