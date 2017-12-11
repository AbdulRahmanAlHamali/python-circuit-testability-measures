def calculateControllability(levels, circuitDescription, testability):
    for level in levels:
        for lineInd in level:
            if testability.get(lineInd) is None:
                testability[lineInd] = {}
            lineInfo = level[lineInd]
            control0 = calculateControllabilityToZero(lineInfo, circuitDescription, testability)
            testability[lineInd]["control0"] = control0
            control1 = calculateControllabilityToOne(lineInfo, circuitDescription, testability)
            testability[lineInd]["control1"] = control1


def calculateControllabilityToZero(lineInfo, circuitDescription, testability):
    gate = lineInfo["leaving"]
    if gate == None:
        control0 = 1
        return control0
    else:
        control0 = 0
        gateType = circuitDescription[2][gate]["type"]
        if gateType == "nand" or gateType == "or":
            for line in circuitDescription[2][gate]["inputs"]:
                control0 = testability[line]["control0"] + control0
            control0 = control0 + 1
            return control0
        elif gateType == "fanout":
            line = circuitDescription[2][gate]["inputs"][0]
            control0 = testability[line]["control0"]
            return control0
        elif gateType == "and" or gateType == "nor":
            line = circuitDescription[2][gate]["inputs"][0]
            control0 = testability[line]["control0"]
            for line in circuitDescription[2][gate]["inputs"]:
                control0 = min(control0, testability[line]["control0"])
            control0 = control0 + 1
            return control0
        elif gateType == "not":
            line = circuitDescription[2][gate]["inputs"][0]
            control0 = testability[line]["control0"] + 1
            return control0
        elif gateType == "buffer":
            line = circuitDescription[2][gate]["inputs"][0]
            control0 = testability[line]["control0"]
            return control0


def calculateControllabilityToOne(lineInfo, circuitDescription, testability):
    gate = lineInfo["leaving"]
    if gate == None:
        control1 = 1
        return control1
    else:
        control1 = 0
        gateType = circuitDescription[2][gate]["type"]

        if gateType == "and" or gateType == "nor":
            for line in circuitDescription[2][gate]["inputs"]:
                control1 = testability[line]["control1"] + control1
            control1 = control1 + 1
            return control1
        elif gateType == "fanout":
            line = circuitDescription[2][gate]["inputs"][0]
            control1 = testability[line]["control1"]
            return control1
        elif gateType == "nand" or gateType == "or":
            line = circuitDescription[2][gate]["inputs"][0]
            control1 = testability[line]["control1"]
            for line in circuitDescription[2][gate]["inputs"]:
                control1 = min(control1, testability[line]["control1"])
            control1 = control1 + 1
            return control1
        elif gateType == "not":
            line = circuitDescription[2][gate]["inputs"][0]
            control1 = testability[line]["control1"] + 1
            return control1
        elif gateType == "buffer":
            line = circuitDescription[2][gate]["inputs"][0]
            control1 = testability[line]["control1"]
            return control1