import time

# This example uses the mtecconnect3dcp library, which now relies on asyncua's synchronous wrapper.
# Make sure to install mtecconnect3dcp: pip install mtecconnect3dcp
from mtecconnect3dcp import Mixingpump, Printhead, Dosingpump

mp = Mixingpump()
mp.connect("opc.tcp://10.129.4.73:4840") # duo-mix 3DCP+
mp.speed = 50 # Hz (20-50Hz)

ph = Printhead()
ph.connect("opc.tcp://10.129.4.74:4840") # flow-matic PX control
ph.speed = 1000 # 1/min

dp = Dosingpump()
dp.connect("opc.tcp://10.129.4.74:4840") # flow-matic PX control
dp.speed = 30 # ml/min



dp.cleaning = True # start cleaning water
time.sleep(1) # wait 1 second
ph.running = True # start printhead motor
time.sleep(1) # wait 1 second
mp.running = True # start mixingpump motor
time.sleep(10) # wait 10 seconds
dp.running = True # start dosing
time.sleep(1) # wait 10 seconds
dp.cleaning = False # stop cleaning water
time.sleep(10) # wait 10 seconds

"""
PRINTING PROCESS RUNNING
"""

dp.cleaning = True # start cleaning water
time.sleep(1) # wait 1 second
dp.running = False # stop dosing
mp.running = False # stop mixingpump motor
time.sleep(5) # wait 5 seconds
for i in range(5):
    ph.running = False # stop printhead motor
    time.sleep(1) # wait 1 second
    ph.running = True # start printhead motor
    time.sleep(4) # wait 4 seconds
ph.running = False # stop printhead motor
dp.cleaning = False # stop cleaning water

