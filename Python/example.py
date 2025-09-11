import time

# This example uses the mtecconnect3dcp library, which now relies on asyncua's synchronous wrapper.
# Make sure to install mtecconnect3dcp: pip install mtecconnect3dcp
from mtecconnect3dcp import Printhead, Dosingpump, Pump, Duomix, DuomixPlus, Smp

mp = DuomixPlus()
mp.connect("10.129.4.73") # duo-mix 3DCP+
mp.speed = 50 # Hz (20-50Hz)

ph = Printhead()
ph.connect("10.129.4.74") # flow-matic PX control
ph.speed = 1000 # 1/min

dp = Dosingpump()
dp.connect("10.129.4.74") # flow-matic PX control
dp.speed = 30 # ml/min



dp.cleaning = True # start cleaning water
time.sleep(1) # wait 1 second
ph.run = True # start printhead motor
time.sleep(1) # wait 1 second
mp.run = True # start mixingpump motor
time.sleep(10) # wait 10 seconds
dp.run = True # start dosing
time.sleep(1) # wait 10 seconds
dp.cleaning = False # stop cleaning water
time.sleep(10) # wait 10 seconds

"""
PRINTING PROCESS RUNNING
"""

dp.cleaning = True # start cleaning water
time.sleep(1) # wait 1 second
dp.run = False # stop dosing
mp.run = False # stop mixingpump motor
time.sleep(5) # wait 5 seconds
for i in range(5):
    ph.run = False # stop printhead motor
    time.sleep(1) # wait 1 second
    ph.run = True # start printhead motor
    time.sleep(4) # wait 4 seconds
ph.run = False # stop printhead motor
dp.cleaning = False # stop cleaning water

