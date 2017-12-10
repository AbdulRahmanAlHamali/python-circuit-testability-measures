import argparse
from create_level_array_from_circuit_description import createLevelArrayFromCircuitDescription
from parse_circuit_description_from_file import parseCircuitDescriptionFromFile
from calculate_controllability import calculateControllability

def calculateTestabilityMeasures(fileName):
    circuitDescription = parseCircuitDescriptionFromFile(fileName)
    levels = createLevelArrayFromCircuitDescription(circuitDescription)
    testability = {}

    calculateControllability(levels, circuitDescription, testability);
    for level in reversed(levels):
        for line_ind in level:
            line_info = level[line_ind]
            observ = calculate_observability(line_info, line_ind, circuitDescription, testability)
            testability[line_ind]["obs"] = observ



    for n in testability:
        testability[n]["testability s0"] = testability[n]["control1"] + testability[n]["obs"]
        testability[n]["testability s1"] = testability[n]["control0"] + testability[n]["obs"]
        # TODO something about 10% project requirment: List	10%	of	most	difficult	to	test	faults
        # TOD calculate testability for xor gate
    print testability

def calculate_observability(line_info, line_ind, circuitDescription, testability):
    gate = line_info["entering"]
    if gate == None:
        obs = 0
        return obs
    else:
        gate_type = circuitDescription[2][gate]["type"]
        output_line = circuitDescription[2][gate]["outputs"]
        if gate_type == "and" or gate_type == "nand":
            obs = testability[output_line[0]]["obs"]
            for line in circuitDescription[2][gate]["inputs"]:
                if line_ind == line:
                    pass
                else:
                    obs = obs + testability[line]["control1"]

            obs = obs + 1
            return obs
        elif gate_type == "or" or gate_type == "nor":
            obs = testability[output_line[0]]["obs"]
            for line in circuitDescription[2][gate]["inputs"]:
                if line_ind == line:
                    pass
                else:
                    obs = obs + testability[line]["control0"]
            obs = obs + 1
            return obs
        elif gate_type == "not":
            obs = testability[output_line[0]]["obs"] + 1
            return obs
        elif gate_type == "fanout":
            obs = testability[output_line[0]]["obs"]
            for line in circuitDescription[2][gate]["outputs"]:
                obs = min(obs, testability[line]["obs"])
            return obs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculates testability measures of a certain circuit")
    parser.add_argument("-f ", "--FileName", help="The name of the bench format file that describes the circuit",
                        type=str, required=True)
    args = parser.parse_args()

    FileName = args.FileName
    calculateTestabilityMeasures(FileName)
