import argparse
from create_level_array_from_circuit_description import createLevelArrayFromCircuitDescription
from parse_circuit_description_from_file import parseCircuitDescriptionFromFile
from calculate_controllability import calculateControllability
from calculate_observability import calculateObservability

def calculateTestabilityMeasures(fileName):
    circuitDescription = parseCircuitDescriptionFromFile(fileName)
    levels = createLevelArrayFromCircuitDescription(circuitDescription)
    testability = {}

    calculateControllability(levels, circuitDescription, testability);
    calculateObservability(levels, circuitDescription, testability);

    for n in testability:
        testability[n]["testability s0"] = testability[n]["control1"] + testability[n]["obs"]
        testability[n]["testability s1"] = testability[n]["control0"] + testability[n]["obs"]
        # TODO something about 10% project requirment: List	10%	of	most	difficult	to	test	faults
        # TOD calculate testability for xor gate
    print testability

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculates testability measures of a certain circuit")
    parser.add_argument("-f ", "--FileName", help="The name of the bench format file that describes the circuit",
                        type=str, required=True)
    args = parser.parse_args()

    FileName = args.FileName
    calculateTestabilityMeasures(FileName)
