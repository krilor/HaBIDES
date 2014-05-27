#
##	Run HaBIDES model
#
#	Kristoffer Lorentsen - 2014
#

import habides as hb
from scitools.std import *

# Init hot water tank
# __init__(self,volume, element, loss, temp, tempin, tempset):
hwt = hb.HotWaterTank(200,3000,70,70,10,70)

dt = 1 
n = 72000 # Tjue timer
#time = range(0,n)
time = linspace(0,20,n)

# Set solution arrays
T = zeros(n)
QE = zeros(n)
Ts = zeros(n)
Vo = zeros(n)

# Initial conditions
T[0] = hwt.T
QE[0] = hwt.QE
Ts[0] = hwt.Ts
Vo[0] = hwt.Vo


# Run model
for i in range(1,n):

	# Change setpoint
	if ((i > 120) and (i < 10800)):
		hwt.Ts = 95
	elif ((i >= 10800) and (i < 3600*11.5)):
		hwt.Ts = 50
	else:
		hwt.Ts = 65
	
	# Add consumption
	if ((i > 7.5*3600) and i < (7.5*3600+1200)):
		hwt.VC = 12.0 / 60.0 # 12 l/min
		hwt.TC = 40
	else:
		hwt.VC = 0

	# Register element power, outflow and temp setpoint
	QE[i] = hwt.QE
	Ts[i] = hwt.Ts
	Vo[i] = hwt.Vo
	
	#Step
	hwt.step(dt)
	
	# Register new temperature
	T[i] = hwt.T

# Plot solution
plot(time, T,'-r',time,(QE / 100),'k--',time,Vo * 100,'-b',time,Ts,'--r')
title('Adjusted temperature setpoint')
legend('T','QE','Vo','Ts')
	