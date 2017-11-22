def parseCircuitDescriptionFromFile(fileName):
	file = open(fileName, 'r')

	inputs = []
	outputs = []
	gates = []
	for line in file:
		if (line.startswith('#')):
			continue
		if (line.startswith('INPUT')):
			inputs.append(line[len('INPUT(') : line.index(')')])
		if (line.startswith('OUTPUT')):
			outputs.append(line[len('OUTPUT(') : line.index(')')])
		if ('=' in line):
			lineWithNoSpaces = "".join(line.split())	#We remove the spaces to make processing easier
			
			gateOutput = [lineWithNoSpaces[0 : lineWithNoSpaces.index('=')]]
			gateType = lineWithNoSpaces[lineWithNoSpaces.index('=') + 1 : lineWithNoSpaces.index('(')]
			gateInputs = lineWithNoSpaces[lineWithNoSpaces.index('(') + 1 : lineWithNoSpaces.index(')')].split(',')
			gates.append({'outputs': gateOutput, 'inputs': gateInputs, 'type': gateType})
	file.close()

	# First, we transform gates so that it accounts for fanout
	# Everytime we find out that there is a fanout, we consider the fanout to be a gate that takes one input and produce multiple outputs
	for gate in gates:
		for i in gate['inputs']:
			# If we find the same input in other gates, then we have a fanout
			# We rename the fanout branches as originalName_counter
			# Then, we create a new gate called a fanout gate
			counter = 0
			originalLineName = i
			foundFanout = False
			for otherGate in gates:
				if i in otherGate['inputs']:
					if otherGate != gate:
						foundFanout = True
						break
					else:
						# The same gate could for whatever reason have a fanout of the same line, we try to detect that
						if (otherGate['inputs'].count(i) > 1):
							foundFanout = True
							break

			if foundFanout == True:
				# Find and replace everywhere
				# And create a fanout gate
				fanoutGate = {'outputs': [], 'inputs': [originalLineName], 'type': 'fanout'}
				for g in gates:
					if (originalLineName in g['inputs'] and g['type'] != 'fanout'):
						for index, inp in enumerate(g['inputs']):
							if (g['inputs'][index] == originalLineName):
								g['inputs'][index] = originalLineName + '_' + str(counter)
								counter += 1
								fanoutGate['outputs'].append(g['inputs'][index])
				gates.append(fanoutGate)

	return (inputs, outputs, gates)