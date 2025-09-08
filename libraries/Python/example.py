import time
from mtecConnectOPCUA import Mixingpump, Printhead, Dosingpump

mp = Mixingpump()
mp.connect("opc.tcp://10.129.4.73:4840") # duo-mix 3DCP+
mp.speed = 50 # % ( = 25Hz)

ph = Printhead()
ph.connect("opc.tcp://10.129.4.74:4840") # flow-matic PX control
ph.speed = 1000 # 1/min

do = Dosingpump()
do.connect("opc.tcp://10.129.4.74:4840") # flow-matic PX control
do.speed = 30 # ml/min



ph.cleaning = True # start cleaning water
time.sleep(1) # wait 1 second
ph.running = True # start printhead motor
time.sleep(1) # wait 1 second
mp.running = True # start mixingpump motor
time.sleep(10) # wait 10 seconds
do.running = True # start dosing
time.sleep(1) # wait 10 seconds
ph.cleaning = False # stop cleaning water
time.sleep(10) # wait 10 seconds

"""
PRINTING PROCESS RUNNING
"""

ph.cleaning = True # start cleaning water
time.sleep(1) # wait 1 second
do.running = False # stop dosing
mp.running = False # stop mixingpump motor
time.sleep(5) # wait 5 seconds
for i in range(5):
    ph.running = False # stop printhead motor
    time.sleep(1) # wait 1 second
    ph.running = True # start printhead motor
    time.sleep(4) # wait 4 seconds
ph.running = False # stop printhead motor
ph.cleaning = False # stop cleaning water

