import argparse
from operator import itemgetter
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
        # TODo calculate testability for xor gate

    sortedTest0=sorted(testability, key=lambda x: (testability[x]['testability s0'], ),reverse= True)
    sortedTest1 = sorted(testability, key=lambda x: (testability[x]['testability s1'],), reverse=True)

    lengthTestability=len(testability)

    x= round (lengthTestability*0.1,0)
    print "highest 10% testabilitys0 "
    for i in range(1,int(x)+1):
         pass
        #print sortedTest0[i]
        ##print testability[sortedTest0[i]]
    print "highest 10% testabilitys1 "
    for i in range(1, int(x) + 1):
        pass
        #print sortedTest1[i]
        #print testability[sortedTest1[i]]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculates testability measures of a certain circuit")
    parser.add_argument("-f ", "--FileName", help="The name of the bench format file that describes the circuit",
                        type=str, required=True)
    args = parser.parse_args()

    FileName = args.FileName
    calculateTestabilityMeasures(FileName)
