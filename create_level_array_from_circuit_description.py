
def createLevelArrayFromCircuitDescription(circuitDescription):
	
	inputs = circuitDescription[0]
	gates = circuitDescription[2]

	levels = [inputs]

	numberOfGatesDone = 0
	while numberOfGatesDone < len(gates):
		newLevel = []
		# We check each gate, if all its inputs exist in some previous level, we add its output to the new level
		for gate in gates:
			if (all(any(i in level for level in levels) for i in gate['inputs'])):
				# all inputs belong to a previous level
				# we check that the outputs of the gate have not been added yet to the levels array
				if (all(o not in level for level in levels for o in gate['outputs'])):
					newLevel.extend(gate['outputs'])
					numberOfGatesDone += 1
		levels.append(newLevel)

	return levels