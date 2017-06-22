import math
import numpy.random as rnd
import matplotlib.pyplot as plt

##We use periodic boundary conditions

##Rules too cool for school
##Rule 15857438548836770733
##Rule 7013446161876011986
##Really cool inverted rule 8751208245429627603
##A boring rule 1078829161419925813
##May be fun if run for long 12788843873880927510
##Inverted rule with structures that suddenly stop 5583078659412628983
##The Staircase 16839147985716303957
##Another brick in the wall 15019984035750327194
##Thin-Thick  17562889651391225768
##Too simple 1680898567611977563
##Single line wandering off into the distance 397332160388432400
##Steep line  13256971636594741960
##Darkness 11272099897237652462
##Triangles everywhere  9221735924566524692
##Inverted rules are cools 8602996565492173401
##Why are inverted rules so common? 17887718470881683859
##Badass 17996963635646362746
##Run for 200 steps 7051835795105380730


state = [] ##state[i] is the vector specifying the state at the ith timestep


width = 100 ## dimensionality of state-vectors
numberOfBlocks = 100 ##Look back numberOfBlocks timestep

def InitializeState(state):
	##Put black state at middle of second row
	state.append([0]*width)
	state.append([0]*width)
	state[1][math.floor(width/2)] = 1
	return state


def GenRandRule():
	##Every state in neighborhood maps to a number between zero and 63
	##This number is used as an index to access the rule vector which tells us what the
	##state at the next timestep should be
	##Thus the rule 
	rule = {j : rnd.randint(2) for j in range(0,64)}

	##There are 2^64 possible rules. We can number these from 0 to 2^64-1.
	rulenumber = 0
	for j in range(0,64):
		rulenumber += 2**(j)*rule[j]

	print('Generated rule number: ', rulenumber)
	return rule

def ConvertRuleNumberToRule(rulenumber):
	for j in range(0,64):
		test = (rulenumber % 2**(j+1) - rulenumber % 2**j)/(2**j)
		if (test != 0 and test != 1):
			print("index error")
			print(rulenumber % 2**(j+1))
			print(rulenumber % 2**(j))
	rule = {j : (rulenumber % 2**(j+1) - rulenumber % 2**j)/(2**j) for j in range(0,64) }
	return rule


def CAStep(state, rule):
	newstate = []
	##Map current state to statenumber
	## 1 2 4
	## 8 16 32

	statenumber = state[-2][width-1] + 2*state[-2][0] + 4*state[-2][1] \
		+ 8*state[-1][width-1] + 16*state[-1][0] + 32*state[-1][1]
	newstate.append(rule[statenumber])		

	for j in range(1,width-1):
		statenumber = state[-2][j-1]+2*state[-2][j] + 4*state[-2][j+1] \
			+ 8*state[-1][j-1] + 16*state[-1][j] + 32*state[-1][j+1]
		newstate.append(rule[statenumber])

	statenumber = state[-2][width-2]+2*state[-2][width-1] + 4*state[-2][0] \
			+ 8*state[-1][width-2] + 16*state[-1][width-1] + 32*state[-1][0]
	newstate.append(rule[statenumber])
	state.append(newstate)

	return



def PlotState(state):
	inind = max(0, len(state)-numberOfBlocks)
	for j in range(0, len(state)):
		for k in range(0,width):
			if (state[j][k] == 0):
				c = "white"
			elif (state[j][k] == 1):
				c = "black"
			else:
				print("Serious error man")
			plt.gcf().gca().add_artist(
				plt.Rectangle((k, numberOfBlocks-j-1), 1, 1, color=c))
	return




if __name__ == '__main__':
	state = InitializeState(state)
	rule = GenRandRule()	
	#rule = ConvertRuleNumberToRule(8751208245429627603)
	numTimeSteps = 100
	numberOfBlocks = numTimeSteps
	
	plt.axis([0, width, 0, numberOfBlocks])
	##plt.ion()
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
	PlotState(state)
	plt.show()
