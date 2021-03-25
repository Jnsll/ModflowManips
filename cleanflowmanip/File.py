import pandas as pd
import os

class File:

    def __init__(self, file_name, file_path):
        self.name = file_name
        self.path = file_path




class InputFile(File):

    def __init__(self, file_name, file_path, approximation, chronicle, reference, rate):
        self.name = file_name
        self.path = file_path
        self.approximation = approximation
        self.chronicle = chronicle
        self.reference = reference
        self.rate = rate

    
    def write_data(self, data):
        pass

    
class H5File(File):

    def __init__(self, file_name, file_path, model, scenario, variable, cell):
        self.name = file_name
        self.path = file_path
        self.model = model
        self.scenario = scenario
        self.variable = variable
        self.cell = cell
    
    def retrieve_data(self):
        self.raw_data = pd.read_hdf(self.path  + "/" + self.name, self.model + '/' + self.variable + '/' + self.scenario)

    def format_data(self):
        formatted_data = pd.DataFrame(columns=["stress_period", "sp_length", "time_step", "study (0 : TS or 1 : SS)", "rech"])
        row = {"stress_period": 0, "sp_length": 1, "time_step":1, "study (0 : TS or 1 : SS)": 1, "rech":float(0.00000)}
        formatted_data = formatted_data.append(row, ignore_index=True)
        nb_stress_period = 1
        for val in self.raw_data["2010-01-01":"2059-12-31"].englobe: #2059-12-31 included
            row = {"stress_period": nb_stress_period, "sp_length": 1, "time_step":1, "study (0 : TS or 1 : SS)":0, "rech":float(val)/1000}
            formatted_data = formatted_data.append(row, ignore_index=True)
            #print(formatted_data)
            nb_stress_period +=1
        self.formatted_data = formatted_data
        
    def store_formatted_data_into_txt_file(self):
        file_name = "input_file_" + str(self.model) + "_" + str(self.variable) + "_" + str(self.scenario) + "_Cell" + str(self.cell) + ".txt"
        self.formatted_data.to_csv("/DATA/These/Projects/modflops/docker-simulation/modflow/data/" + file_name, sep="\t", index=False)
        
        # Updating file with names of reference input files
        file_references_chronicles = pd.read_csv(os.path.join("/DATA/These/Projects/modflops/docker-simulation/modflow", "data", "chronicles.txt"), sep=",")
        #print(file_references_chronicles["template"].tolist())
        if file_name in file_references_chronicles["template"].tolist():
            print("File '" + file_name + "' has already been stored.")
        else:
            row= {"number":len(file_references_chronicles), "chronicle": "GIEC_" + str(self.model) + "_" + str(self.variable) + "_" + str(self.scenario) + "_Cell" + str(self.cell), "template" : file_name}
            file_references_chronicles = file_references_chronicles.append(row, ignore_index=True)
            print(file_references_chronicles)
            file_references_chronicles.to_csv(os.path.join("/DATA/These/Projects/modflops/docker-simulation/modflow", "data", "chronicles.txt"), sep=",", index=False)


    def get_formatted_data(self):
        formatted_data = self.formatted_data
        return formatted_data