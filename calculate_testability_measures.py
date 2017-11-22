import argparse
from create_level_array_from_circuit_description import createLevelArrayFromCircuitDescription
from parse_circuit_description_from_file import parseCircuitDescriptionFromFile

def calculateTestabilityMeasures(fileName):
	circuitDescription = parseCircuitDescriptionFromFile(fileName)
	levels = createLevelArrayFromCircuitDescription(circuitDescription)
	print levels
	
if __name__ == '__main__':

	parser = argparse.ArgumentParser(description = "Calculates testability measures of a certain circuit")
	parser.add_argument("-f ","--FileName", help = "The name of the bench format file that describes the circuit", type = str, required = True)
	args = parser.parse_args()
	
	FileName = args.FileName
	calculateTestabilityMeasures(FileName)