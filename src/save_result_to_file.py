def saveResultToFile(fileName, circuitDescription, testability, hardest10PercentS0, hardest10PercentS1):
	file = open(fileName, 'w')
	file.write('*******************************************************\n')
	file.write('\nCircuit Description:\n\n')
	file.write('\tInputs:\n')
	for input in circuitDescription[0]:
		file.write('\t\t' + input + '\n')
	file.write('\tOutputs:\n')
	for output in circuitDescription[1]:
		file.write('\t\t' + output + '\n')
	file.write('\tGates:\n')
	for gate in circuitDescription[2]:
		gateString = '(' + ', '.join(circuitDescription[2][gate]['outputs']) + ')'
		gateString += ' = ' + circuitDescription[2][gate]['type']
		gateString += '(' + ', '.join(circuitDescription[2][gate]['inputs']) + ')'
		file.write('\t\t' + gateString + '\n')
	file.write('*******************************************************\n')
	file.write('\nTestability:\n\n')
	file.write('Line Name'.ljust(15) + 'CC0'.ljust(6) + 'CC1'.ljust(6) + 'CO' + '\n')
	file.write('-----------------------------\n')
	for line in testability:
		lineString = line.ljust(15)
		lineString += str(testability[line]['control0']).ljust(6)
		lineString += str(testability[line]['control1']).ljust(6)
		lineString += str(testability[line]['obs'])
		file.write(lineString + '\n')
	file.write('*******************************************************\n')
	file.write('\nTop 10% Hardest Lines to Test:\n\n')
	file.write('S0: ' + ', '.join(hardest10PercentS0) + '\n')
	file.write('S1: ' + ', '.join(hardest10PercentS1) + '\n')
	file.close()