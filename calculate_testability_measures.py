import argparse
from create_level_array_from_circuit_description import createLevelArrayFromCircuitDescription
from parse_circuit_description_from_file import parseCircuitDescriptionFromFile

testability = {}


def calculateTestabilityMeasures(fileName):
    circuitDescription = parseCircuitDescriptionFromFile(fileName)
    print ("circuit description input output gates:")
    print(circuitDescription)
    levels = createLevelArrayFromCircuitDescription(circuitDescription)
    print "levels"
    print levels


    for level in levels:

        for line_ind in level:
            if testability.get(line_ind) is None:
                testability[line_ind] = {}
            line_info= level[line_ind]
            control0=calculate_cont_zero(line_info,circuitDescription)
            testability[line_ind]["control0"]=control0
            control1=calculate_cont_one(line_info,circuitDescription)
            testability[line_ind]["control1"] = control1
    for level in reversed(levels):
        for line_ind in level:
            line_info = level[line_ind]
            observ=calculate_observability(line_info,line_ind,circuitDescription)
            testability[line_ind]["obs"]=observ

    print testability


def calculate_cont_zero(line_info,circuitDescription):

    gate=line_info["leaving"]
    if gate==None:

        control0=1
        return control0
    else:
        control0=0
        gate_type=circuitDescription[2][gate]["type"]
        if gate_type=="nand" or gate_type=="or":
            for line in  circuitDescription[2][gate]["inputs"]:
                control0=testability[line]["control0"]+control0
            control0=control0+1
            return control0
        if gate_type=="fanout":
            line = circuitDescription[2][gate]["inputs"][0]
            control0=testability[line]["control0"]
            return control0
        if gate_type=="and"or gate_type=="nor":
            line=circuitDescription[2][gate]["inputs"][0]
            control0 = testability[line]["control0"]
            for line in  circuitDescription[2][gate]["inputs"]:
                control0=min(control0,testability[line]["control0"])
            control0=control0+1
            return control0
        if gate_type=="not":
            line = circuitDescription[2][gate]["inputs"][0]
            control0=testability[line]["control0"]+1
            return control0


def calculate_cont_one(line_info,circuitDescription):

    gate=line_info["leaving"]
    if gate==None:

        control1=1
        return control1
    else:
        control1=0
        gate_type=circuitDescription[2][gate]["type"]

        if gate_type=="and" or gate_type=="nor":
            for line in  circuitDescription[2][gate]["inputs"]:
                control1=testability[line]["control1"]+control1
            control1=control1+1
            return control1
        if gate_type=="fanout":
            line = circuitDescription[2][gate]["inputs"][0]
            control1=testability[line]["control1"]
            return  control1
        if gate_type=="nand"or gate_type=="or":
            line=circuitDescription[2][gate]["inputs"][0]
            control1 = testability[line]["control1"]
            for line in  circuitDescription[2][gate]["inputs"]:
                control1=min(control1,testability[line]["control1"])
            control1=control1+1
            return control1
        if gate_type=="not":
            line = circuitDescription[2][gate]["inputs"][0]
            control1=testability[line]["control1"]+1
            return control1


def calculate_observability(line_info,line_ind,circuitDescription):
    gate=line_info["entering"]
    print line_ind
    if gate==None:
        obs=0
        return obs
    else:

        gate_type = circuitDescription[2][gate]["type"]
        output_line=circuitDescription[2][gate]["outputs"]
        if gate_type=="and" or gate_type=="nand":
            obs=testability[output_line[0]]["obs"]
            for line in  circuitDescription[2][gate]["inputs"]:
                if line_ind==line:
                    pass
                else:
                    obs=obs+testability[line]["control1"]

            obs=obs+1
            print obs
            return obs
        if gate_type=="or" or gate_type=="or":
            obs=testability[output_line[0]]["obs"]
            for line in  circuitDescription[2][gate]["inputs"]:
                if line_ind==line:
                    pass
                else:
                    obs=obs+testability[line]["control0"]
            obs=obs+1
            print obs
            return obs
        if gate_type=="not":
            obs = testability[output_line[0]]["obs"]+1
            print obs
            return obs
        if gate_type=="fanout":
            obs = testability[output_line[0]]["obs"]
            for line in circuitDescription[2][gate]["outputs"]:
                obs=min(obs,testability[line]["obs"])
            print obs
            return obs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Calculates testability measures of a certain circuit")
    parser.add_argument("-f ", "--FileName", help="The name of the bench format file that describes the circuit",
                        type=str, required=True)
    args = parser.parse_args()

    FileName = args.FileName
    calculateTestabilityMeasures(FileName)
