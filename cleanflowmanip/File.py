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


    def create_file(self):
        pass


class H5File(File):

    def __init__(self, file_path, model, scenario, variable, cell):
        self.name = "SURFEX_" + str(model) + "_Cell_"+ str(cell) +"_" + str(scenario) + ".h5"
        self.path = file_path
        self.model = model
        self.scenario = scenario
        self.variable = variable
        self.cell = cell
    
    def retrieve_data(self):
        self.raw_data = pd.read_hdf(self.path  + "/" + self.name, self.model + '/' + self.variable + '/' + self.scenario)

    def format_data(self):
        self.formatted_data = pd.DataFrame(columns=["stress_period", "sp_length", "time_step", "study (0 : TS or 1 : SS)", "rech"])
        self.set_first_row_of_formatted_data()
        self.fill_rows_of_formatted_data_dataframe()

    def set_first_row_of_formatted_data(self):
        row = {"stress_period": 0, "sp_length": 1, "time_step":1, "study (0 : TS or 1 : SS)": 1, "rech":float(0.00000)}
        self.formatted_data = self.formatted_data.append(row, ignore_index=True)

    def fill_rows_of_formatted_data_dataframe(self):
        nb_stress_period = 1
        for value in self.raw_data["2010-01-01":"2059-12-31"].englobe: #2059-12-31 included
            row = {"stress_period": nb_stress_period, "sp_length": 1, "time_step":1, "study (0 : TS or 1 : SS)":0, "rech":float(value)/1000}
            self.formatted_data = self.formatted_data.append(row, ignore_index=True)
            nb_stress_period += 1

    def store_formatted_data_into_reference_file(self):
        reference_file_name = self.create_reference_file()
        self.update_chronicles_file_with_reference_file_name(reference_file_name)        

    def create_reference_file(self):
        file_name = "input_file_" + str(self.model) + "_" + str(self.variable) + "_" + str(self.scenario) + "_Cell" + str(self.cell) + ".txt"
        self.formatted_data.to_csv("/DATA/These/Projects/modflops/docker-simulation/modflow/data/" + file_name, sep="\t", index=False)
        return file_name

    def update_chronicles_file_with_reference_file_name(self, reference_file_name):
        #reference_file_name = self.get_reference_file_name()
        # Updating file with names of reference input files
        file_references_chronicles = pd.read_csv(os.path.join("/DATA/These/Projects/modflops/docker-simulation/modflow", "data", "chronicles.txt"), sep=",")
        if reference_file_name in file_references_chronicles["template"].tolist():
            print("File '" + reference_file_name + "' has already been stored.")
        else:
            row = {"number":len(file_references_chronicles), "chronicle": "GIEC_" + str(self.model) + "_" + str(self.variable) + "_" + str(self.scenario) + "_Cell" + str(self.cell), "template" : reference_file_name}
            file_references_chronicles = file_references_chronicles.append(row, ignore_index=True)
            file_references_chronicles.to_csv(os.path.join("/DATA/These/Projects/modflops/docker-simulation/modflow", "data", "chronicles.txt"), sep=",", index=False)

    def get_reference_file_name(self):
        return "input_file_" + str(self.model) + "_" + str(self.variable) + "_" + str(self.scenario) + "_Cell" + str(self.cell) + ".txt"

    def get_formatted_data(self):
        formatted_data = self.formatted_data
        return formatted_data