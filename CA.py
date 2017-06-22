import random
import math
import matplotlib.pyplot as plt
#--------------------------
#--------------------------
#--------------------------
## CA specs

# Total number of neurons
N = 100;

# Number of excitatory neurons
N_e = math.floor(0.9*N)

# Number of fast inhibitory neurons
N_f = math.floor(0.05*N)

# Number of slow inhibitory neurons
N_s = math.floor(0.05*N)


# Number of connections for (e)
z_e = 20

# Number of connections for (f)
z_f = 200

# Number of connections for (s)
z_s = 200

# Bond strengths
K_e = 1
K_f = 10
K_s = 10

# Delay times
t_de = 10
t_df = 1
t_ds = 25
maxTime = max(t_de,t_df,t_ds)

# Firing duration
phi_e = 20
phi_f = 20
phi_s = 100

# Refractory period
rho = 700

# Spontaneous firing time max and min
spontmax = 11
spontmin = 10

# Typical values of the refractory period is 700-900 and for spontaneous firing time
# 900-1200

# Firing Threshold
F = 20

#--------------------------
#--------------------------
#--------------------------

# Utility functions

def ThresholdFunction(neuron):
	if neuron.alpha >= rho:
		return 0
	else:
		return F*(rho-neuron.alpha)/rho


def ShowNeurons(listOfExcitatoryNeurons, listOfFastInhibitoryNeurons, listOfSlowInhibitoryNeurons):
	allNeurons = listOfExcitatoryNeurons + listOfSlowInhibitoryNeurons + listOfFastInhibitoryNeurons
	nE = math.ceil(math.sqrt(len(listOfExcitatoryNeurons)))
	nF = math.ceil(math.sqrt(len(listOfFastInhibitoryNeurons)))
	nS = math.ceil(math.sqrt(len(listOfSlowInhibitoryNeurons)))
	plt.axis([-1, nE+nF+nS+5, -1, nE+nF+nS+5])

	for j in range(0,len(listOfExcitatoryNeurons)):
		if listOfExcitatoryNeurons[j].states[-1] == 0:
			c = "white"
		else:
			c = "black"
		plt.gcf().gca().add_artist(plt.Circle(((j-j%nE)/nE,j%nE), 0.2, color=c, ec = "black"))

	for j in range(0, len(listOfFastInhibitoryNeurons)):
		if listOfFastInhibitoryNeurons[j].states[-1] == 0:
			c = "blue"
		else: 
			c = "black"
		plt.gcf().gca().add_artist(plt.Circle(((j-j%nF)/nF+nE/2,j%nF+nE+2), 0.2, color = c, ec = "black"))

	for j in range(0, len(listOfSlowInhibitoryNeurons)):
		if listOfSlowInhibitoryNeurons[j].states[-1] == 0:
			c = "green"
		else:
			c = "black"
		plt.gcf().gca().add_artist(plt.Circle(((j-j%nS)/nS+nF+nE, j%nS), 0.2, color=c, ec = "black"))


## The Neuron classes

class Neuron:
	def __init__(self):
		self.newState = 0
		self.states = []
		self.neighbors = []
		self.connections = []


	def ShiftStates(self):
		for j in range(0,len(self.states)-1):
			self.states[j] = self.states[j+1]


	def FindConnections(self, listOfAllNeurons)
:		while len(self.connections) < z_e:
			index = random.randrange(0,len(listOfAllNeurons))
			if listOfAllNeurons[index] != self: # Maybe remove this restriction?
				self.connections.append(listOfAllNeurons[index])

	def FindNeighbors(self,listOfAllNeurons):
		for neuron in listOfAllNeurons:
			if self in neuron.connections:
				self.neighbors.append(neuron)
	def FinalUpdate(self):
		self.ShiftStates()
		self.states[-1] = self.newState

	


class ExcitatoryNeuron(Neuron):
	# Spontaneous firing time



	def __init__(self):
		Neuron.__init__(self)
		self.alpha = 1
		self.sigma = random.randrange(spontmin, spontmax)
		for j in range(0,maxTime):
			self.states.append(0)

	def Update(self):
		if (self.states[-1] > 0 or self.states[-2] > 0):
			self.newState = self.states[-1] +1 % phi_e+1
			print("TESTTEST")

		elif self.states[-1] == 0:
			if self.alpha >= self.sigma:
				self.newState = 1
				self.alpha = 1
			else: 
				input = 0
				for n in self.neighbors:
					input += n.Output()
				if input > ThresholdFunction(self):
					print("Threshold exceeded")
					self.newState = 1
					self.alpha = 1
				else:
					self.alpha += 1
					self.newState = 0




	def Output(self):
		if self.states[1-t_de] > 0:
			return K_e
		else:
			return 0
	




class InhibitoryNeuron(Neuron):

	def __init__(self, type):
		Neuron.__init__(self)
		if type == "slow":
			self.delay = t_ds
			self.K = K_s
			self.phi = phi_s
		elif type == "fast":
			self.delay = t_df
			self.K = K_f
			self.phi = phi_f
		else:
			print("Invalid Type")
		for j in range(0,maxTime):
			self.states.append(0)

	def Update(self):
		if self.states[-1] == 0:
			self.newState = 0
			for n in self.neighbors:
				if type(n) == ExcitatoryNeuron:
					if n.states[-1-1] > 0:
						self.newState = 1
						break;

		else:
			self.newState = self.states[-1] + 1 % self.phi+1
			

	def Output(self):
		if self.states[1-self.delay] > 0:
			return -self.K
		else:
			return 0





if __name__ == "__main__":
	eneurons = []
	fneurons = []
	sneurons = []

	for j in range(0,N_e):
		eneurons.append(ExcitatoryNeuron())
	for j in range(0,N_f):
		fneurons.append(InhibitoryNeuron("fast"))
	for j in range(0, N_s):
		sneurons.append(InhibitoryNeuron("slow"))

	AllNeurons = eneurons + fneurons + sneurons

	eneurons[0].FindConnections(AllNeurons)
	fneurons[0].FindNeighbors(AllNeurons)

	for k in range(0,3):
		print(eneurons[k].sigma)
	
	for k in range(0,1000):
		print("k = ", k)
		for j in range(0,len(AllNeurons)):
			AllNeurons[j].Update()
		for j in range(0,len(AllNeurons)):
			AllNeurons[j].FinalUpdate()

		print("-"*10)
		for j in range(0,3):
			print("alpha = ", eneurons[j].alpha)
			print("number of states = ", len(eneurons[j].states))
			print("states = ", eneurons[j].states)
			print("newState = ", eneurons[j].newState)

		print("-"*10)
		for j in range(0,3):
			if eneurons[j].states[-1] == 1:
				print("Activate")
			else:
				print("Inactive");

		print("-"*10)
		ShowNeurons(eneurons, fneurons, sneurons)
		plt.show()
	


	# I think there is some weird cross-comm between different instances of the
	# neuron classes