import math
import numpy.random as rnd
import matplotlib.pyplot as plt
import time

##We use periodic boundary conditions


##Cools rules


##Rules with simple behavior
##11579
##1695
##17877
##15034
##13832
##51788

state = [] ##state[i] is the vector specifying the state at the ith timestep


width = 200 ## dimensionality of state-vectors
numberOfBlocks = 100 ##Look back numberOfBlocks timestep

def InitializeState(state):
	##Put black state at middle of second row
	state.append([0]*width)
	state.append([0]*width)
	state[1][math.floor(width/2)] = 1
	return state

def InitializeRandomState(state):
	state.append([0]*width)
	state.append([rnd.randint(2) for j in np.arange(width)])
	return state


def GenRandRule():
	##Every state in neighborhood maps to a number between zero and 15
	##This number is used as an index to access the rule vector which tells us what the
	##state at the next timestep should be
	##Thus the rule 
	rule = {j : rnd.randint(2) for j in range(0,16)}

	##There are 2^64 possible rules. We can number these from 0 to 2^64-1.
	rulenumber = 0
	for j in range(0,16):
		rulenumber += 2**(j)*rule[j]

	print('Generated rule number: ', rulenumber)
	return [rule, rulenumber]

def ConvertRuleNumberToRule(rulenumber):
	for j in range(0,16):
		test = (rulenumber % 2**(j+1) - rulenumber % 2**j)/(2**j)
		if (test != 0 and test != 1):
			print("index error")
			print(rulenumber % 2**(j+1))
			print(rulenumber % 2**(j))
	rule = {j : (rulenumber % 2**(j+1) - rulenumber % 2**j)/(2**j) for j in range(0,16) }
	return rule


def CAStep(state, rule):
	newstate = []
	##Map current state to statenumber
	## 1 2 4
	## 8 16 32

	statenumber = state[-2][width-1] + 2*state[-2][0] + 4*state[-2][1] \
					+ 8*state[-1][0]
	newstate.append(rule[statenumber])		

	for j in range(1,width-1):
		statenumber = state[-2][j-1]+2*state[-2][j] + 4*state[-2][j+1] \
					+ 8*state[-1][j]
		newstate.append(rule[statenumber])

	statenumber = state[-2][width-2]+2*state[-2][width-1] + 4*state[-2][0] \
							+ 8*state[-1][width-1]
	newstate.append(rule[statenumber])
	state.append(newstate)

	return



def PlotState(state, fig):
	inind = max(0, len(state)-numberOfBlocks)
	for j in range(0, len(state)):
		for k in range(0,width):
			if (state[j][k] == 0):
				c = "white"
			elif (state[j][k] == 1):
				c = "black"
			else:
				print("Serious error man")
			fig.gca().add_artist(
				plt.Rectangle((k, numberOfBlocks-j-1), 1, 1, color=c))
	return




if __name__ == '__main__':
	for j in range(0,15):
		state = []
		state = InitializeState(state)
		[rule, rulenumber] = GenRandRule()	
		#rule = ConvertRuleNumberToRule(8751208245429627603)
		numTimeSteps = 200
		numberOfBlocks = numTimeSteps
		
		plt.ion()
		for j in range(0, len(state)):
			for k in range(0,width):
				if (state[j][k] == 0):
					c = "white"
				else:
					c = "black"
				plt.gcf().gca().add_artist(
					plt.Rectangle((k, numberOfBlocks-j-1), 1, 1, color=c))


		for j in range(0, numTimeSteps):
			CAStep(state,rule)
			
			##plt.pause(0.05)
		print('Evolution done')
		t1 = time.time()
		fig = plt.figure()
		PlotState(state, fig)
		plt.axis([0, width, 0, numberOfBlocks])
		fig.show()
		fig.savefig('LightConeRuns/' + str(rulenumber) + '.png')
		t2 = time.time()
		print('Figure saved. Time spent: ', t2-t1)
		plt.close(fig)
		t3 = time.time()
		print('Figure closed. Time spent: ', t3-t2)
		#plt.show()
