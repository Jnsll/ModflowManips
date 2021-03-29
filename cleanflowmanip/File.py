import pandas as pd
import numpy as np
import os

class File:

    def __init__(self, file_name, file_path):
        self.name = file_name
        self.path = file_path

    def get_chronicles_config_from_file(self):
        file_references_chronicles = pd.read_csv(os.path.join("/DATA/These/Projects/modflops/docker-simulation/modflow", "data", "chronicles.txt"), sep=",")
        return file_references_chronicles

    def set_modflow_app_folder_path(self, modflow_app_folder_path):
        self.modflow_folder_path = modflow_app_folder_path

class InputFile(File):

    def __init__(self, approximation, chronicle, reference, rate):
        self.approximation = approximation
        self.chronicle = chronicle
        self.reference = reference
        self.rate = rate


    def generate_custom_input_file(self, model_name, input_name, steady):
        chronicle_file = pd.read_table(os.path.join(self.modflow_folder_path, "data", "chronicles.txt"), sep=',', header=0, index_col=0) #"/DATA/These/Projects/modflops/docker-simulation/modflow"
        reference_file = chronicle_file.template[self.chronicle]
        self.manipulate_ref_input_file(reference_file, steady)
        model_name = self.get_model_name(model_name)
        self.write_custom_input_file(model_name)

    def manipulate_ref_input_file(self, reference_file_name, steady_simulation): #, periodValue
        self.reference_data = self.extract_df_from_ref_input_file(reference_file_name)
        
        if steady_simulation :
            self.create_custom_dataframe_for_steady_simulation_from_reference_dataframe()
        else:
            self.create_custom_dataframe_for_transitory_simulation_from_reference_dataframe()

    def extract_df_from_ref_input_file(self, reference_file_name):
        input_path = os.path.join(self.modflow_folder_path, "data", reference_file_name)
        df = pd.read_csv(input_path, sep='\t', dtype=np.float64)
        return df

    def create_custom_dataframe_for_steady_simulation_from_reference_dataframe(self):
        self.custom_data = self.reference_data
        self.set_mean_recharge_for_initialisation_steady_stress_period() #df['rech'][0]
        self.custom_data = self.custom_data.iloc[[0]]

    def set_mean_recharge_for_initialisation_steady_stress_period(self):
        self.custom_data.loc[0,'rech'] = float(self.custom_data['rech'].mean()) #df['rech'][0]
        print("mean init for inputfile: ", self.custom_data.loc[0,'rech'])

    def create_custom_dataframe_for_transitory_simulation_from_reference_dataframe(self):
        self.custom_data = self.reference_data
        if self.approximation==0:
            period = [int(self.rate)] #getNumberOfLinesToReduceInLoop(prd)
            indexes = self.get_indexes_to_remain_in_custom_file(len(self.custom_data.index), period)
        # elif self.approximation==1:
        #     indexes = self.get_indexes_to_remain_for_rech_threshold(self.custom_data, len(self.custom_data.index), self.rate)
        # elif self.approximation==2:
        #     period = [int(self.rate)]
        #     indexes = self.get_indexes_to_remain_in_custom_file(len(self.custom_data.index), period) #get_indexes_to_remain_approx3(len(df.index), period)
        else:
            print("The number chosen for the approximation is not valid.") 

        self.aggregate_values(indexes, len(self.custom_data.index))
        self.keep_only_rows_with_indexes(indexes)
        

    def get_indexes_to_remain_in_custom_file(self, number_lines, period):
        ligne = 1
        indexes = [0,1]
        taille_period = len(period)
        i = 0
        while (ligne < number_lines-1):
            ligne += period[i]
            if (ligne < number_lines-1):
                indexes.append(ligne)
            if (i == (taille_period-1)):
                i = 0
            else:
                i += 1
        return indexes

    def aggregate_values(self, indexes, nb_rows):
        '''
            TODO
        '''
        if self.approximation ==2:
            self.aggregate_values_for_approximation_2(indexes, nb_rows)
        else:
            self.aggregate_values_of_custom_data(indexes, nb_rows)

    def aggregate_values_for_approximation_2(self, indexes, nb_rows):
        for i in range(1, len(indexes)):
            if i < (len(indexes)-1):
                self.custom_data.iat[indexes[i], 1] = indexes[i+1] - indexes[i]
            else:
                self.custom_data.iat[indexes[i], 1] = nb_rows - indexes[i]

    def aggregate_values_of_custom_data(self, indexes, nb_rows):
        for i in range(1, len(indexes)):
            #Initialisation has to remain so strating at period number 1. Initialisation period is number 0.
            if i < (len(indexes)-1):
                for z in range(indexes[i]+1, indexes[i+1]): #+1 pour ne pas compter la valeur df.iat[indexes[i]] une deuxième fois
                    self.custom_data.iat[indexes[i], 4] += self.custom_data['rech'][z]
                self.custom_data.iat[indexes[i], 4] = float(self.custom_data.iat[indexes[i], 4]) / (indexes[i+1] - indexes[i])
                self.custom_data.iat[indexes[i], 1] = indexes[i+1] - indexes[i]
            else:
                for z in range(indexes[i]+1, nb_rows):
                    self.custom_data.iat[indexes[i], 4] += self.custom_data['rech'][z]
                self.custom_data.iat[indexes[i], 4] = self.custom_data.iat[indexes[i], 4] / (nb_rows - indexes[i])
                self.custom_data.iat[indexes[i], 1] = nb_rows - indexes[i]

    def keep_only_rows_with_indexes(self, indexes):
        index_remove = []
        for y in range(0, len(self.custom_data.index)):
            index_remove.append(y)

        for z in indexes[:]:
            if z in index_remove:
                index_remove.remove(z)

        self.custom_data.drop(self.custom_data.index[index_remove], inplace=True)

    def get_model_name(self, model_name):
        if model_name is None:
            model_name = "Step1_Chronicle" + str(self.chronicle) + "_Approx" + str(self.approximation) + "_Period" + str(self.rate)
        return model_name

    def write_custom_input_file(self, model_name):
        output_name = "input_file_" + model_name + ".txt"
        file_path = os.path.join(self.modflow_folder_path, "data", output_name)
        self.custom_data.to_csv(file_path, sep="\t", index=False)
        self.name = output_name
        self.path = os.path.join(self.modflow_folder_path, "data")
        print("custom input file name : ", file_path)


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