from math import *
#
###	HaBIDES - Heat and Battery Integrated Domestic Energy Storage
#
#	Model and module by Kristoffer Lorentsen - 2014 
#
#


#
##	Habides Class
#
#	This is the main model class and object initialized with a HW Tank and HW Consumption
#


##	Hot Water Tank Class
#
#	The HWT object holds all the information about the Hot Water Tank - everything from it physical variables to it's states
#

class HotWaterTank:

	# Variables
	yW = 1.0 # Specific weight of water [kg/l]
	CW = 4184.0 # Heat capacity of water [J/degC*KG]
	V = 0.0 # Volume of tank [l]
	PE = 0.0 # Heater element power [W]
	Ti = 0.0 # Water input temperature [degC]
	QL = 0.0 # Heat loss [W]
	QE = 0.0 # Heater element power [W]
	T = 0.0 # Temperature in tank [degC]
	Ts = 0.0 # Setpoint temperature [degC]
	Te = 0.0 # Environment temperature
	U = 0.0 # Energy in tank [J]
	uE = 0.0 # Regulator variable
	TC = 0.0 # Temperature of consumed water [degC]
	VC = 0.0 # Flow of consumed water [l/s] 
	Vo = 0.0 # Flow of water out of tank [l/s]
	
	# Initialize variables
	def __init__(self,volume, element, lossconst, temp, tempin, tempset, tempenv):
	
		# Tank and site variable values
		self.V = volume
		self.PE = element
		self.Ti = tempin
		self.KL = lossconst
		self.Te = tempenv
		
		# Set start temperature and calculate energy content from temperature
		self.T = temp
		self.Ts = tempset
		self.U = self.tempToEnergy(temp)
		
		# Set initial state of heater element using the built in regulator
		self.setRegulator()
		
		# Set initial loss
		self.setLoss()
	
	# Set consumption based on TC and VC
	def setConsumption(self):
	
		# If consumption temperature is higher than tank temperature, reduce to tank temp
		if self.T < self.TC:
			Tcon = self.T
		else:
			Tcon = self.TC
		
		# Calculate consumption volume
		self.Vo = self.VC * ( (Tcon - self.Ti) / (self.T - self.Ti) )
	
	# Set loss based on T and Te
	def setLoss(self):
		self.QL = self.KL*(self.T - self.Te)
		
	
	# Step one timesteps forward at interval dt [s]
	def step(self, dt):
	
		# Set consumtions
		self.setConsumption()
		
		# Set loss
		self.setLoss()
		
		# Calculate change in energy and temp
		dU = (self.Ti - self.T)*self.Vo*self.yW*self.CW + self.QE - self.QL
		self.U = self.U + dU * dt
		
		# Update temp and regulator
		self.T = self.energyToTemp(self.U)
		self.setRegulator()
	
	# Calculate energy content from temperature
	def tempToEnergy(self, temp):
		return	temp * (self.yW*self.CW*self.V)
	
	# Calculate temperature from energy content
	def energyToTemp(self, energy):
		return energy / (self.yW*self.CW*self.V)
	
	# Set regulator
	def setRegulator(self):
		# Set a limit for switching on/of [degC]
		tLim = 1
		
		# Using a standard on/off regulator
		if ((self.uE == 0) and ( self.T < self.Ts - tLim )):
			self.uE = 1;
		elif ((self.uE == 1) and ( self.T > self.Ts + tLim)):
			self.uE = 0;
		
		# Activate/deactivate element
		self.QE = self.uE * self.PE
			
			
#
##	HotWaterConsumption
#
#	Within the HWC object, consumption data is stored. Consumption is given as listed below.
#	Consumption types:
#	0 - none
#	1 - midpoint - flow only
#	2 - 

class HotWaterConsumption:
	
	type = 0 # As listed above
	interval = 0 # Interval for each data point [s]
	inputflow = [] # Raw input flow data
	inputtemp = [] # Raw input temperature data
	modelflow = [] # Flow data for the model
	modeltemp = [] # Temperature data for the model
	
	# Initialize object
	def __init__(self,type,interval,inflow,intemp):
		
		# Set variables
		self.type = type
		self.interval = interval
		
		# Midpoint - flow only
		if type == 1:
			self.inputflow = [float(inflow[i]) for i in range(0,len(inflow))]
			self.inputtemp = [float(intemp) for i in range(0,len(inflow))]
			self.LinearInterp('midflow')
		else:
			print 'ERROR - The input type is not recognized'

	def LinearInterp(self,mode):
	
		# Interp using midpoint - assume that start is zero
		if mode == 'midflow':

			
			# Setup local variables
			l = 0 # Counting variable
			interval = self.interval
			halfint = int(floor(interval / 2))
			
			# Set up flow and temp arrays
			self.modelflow = [0.0 for i in range(0,len(self.inputflow)*interval + 1)]
			self.modeltemp = [self.inputtemp[0] for i in range(0,len(self.inputflow)*interval + 1)]
			
			# Set up first value point
			for i in range(0,halfint):
				self.modelflow[l+1] = self.modelflow[0] + ( (self.inputflow[0] - self.modelflow[0]) / halfint ) * (i + 1)
				self.modeltemp[l+1] = self.inputtemp[0]
				l = l+1
				
			# Linearize between all the following ones
			for i in range(1,len(self.inputflow)):
				for j in range(0,interval):
					self.modelflow[l+1] = self.inputflow[i-1] + ( (self.inputflow[i] - self.inputflow[i-1]) / interval ) * (j + 1)
					self.modeltemp[l+1] = self.inputtemp[0]
					l = l+1
					
			# Trail of to zero again
			for i in range(0,halfint):
				self.modelflow[l+1] = self.inputflow[-1] + ( ( 0 - self.inputflow[-1]) / halfint ) * (i + 1)
				l = l+1
		else:
			print 'Interp mode not recognized'



		