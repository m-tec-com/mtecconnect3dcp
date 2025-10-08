from .MixingpumpPlus import MixingpumpPlus
from .Smp import Smp

class SmpPlus(Smp, MixingpumpPlus):
    """
    SMP

    OPC-UA client class for m-tec SMP machines (Mixingpump).
    Inherits from Smp and MixingpumpPlus.
    """