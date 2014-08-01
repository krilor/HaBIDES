# HaBIDES testing

import habides as hb
from scitools.std import *

# __init_(self,type,interval,inflow,intemp):
cons = hb.HotWaterConsumption(1,3600,[2.0,4.0,3.0,5.0,1.0,7.0,8.0,0.0,10.0],40)

test = range(0, len(cons.modelflow))

plot(test, cons.modelflow,'k--')
show()