#
##	HaBIDES - Heat and Battery Integrated Domestic Energy Storage
#
#	Model and module by Kristoffer Lorentsen - 2014 
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
	U = 0.0 # Energy in tank [J]
	uE = 0.0 # Regulator variable
	TC = 0.0 # Temperature of consumed water [degC]
	VC = 0.0 # Flow of consumed water [l/s] 
	Vo = 0.0 # Flow of water out of tank [l/s]
	
	# Initialize variables
	def __init__(self,volume, element, loss, temp, tempin, tempset):
	
		# Tank and site variable values
		self.V = volume
		self.PE = element
		self.Ti = tempin
		self.QL = loss
		
		# Set start temperature and calculate energy content from temperature
		self.T = temp
		self.Ts = tempset
		self.U = self.tempToEnergy(temp)
		
		# Set initial state of heater element using the built in regulator
		self.setRegulator()
	
	# Set consumption based on TC and VC
	def setConsumption(self):
	
		# If consumption temperature is higher than tank temperature, reduce to tank temp
		if self.T < self.TC:
			Tcon = self.T
		else:
			Tcon = self.TC
		
		# Calculate consumption volume
		self.Vo = self.VC * ( (Tcon - self.Ti) / (self.T - self.Ti) )
	
	# Step one timesteps forward at interval dt [s]
	def step(self, dt):
	
		# Set consumtions
		self.setConsumption()
		
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
			
			
		
		