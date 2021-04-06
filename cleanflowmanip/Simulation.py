import pandas as pd
import os
import flopy
import numpy as np

class Simulation:
    """
        A simulation has several informations:
        - approximation
        - chronicle : int
        - rate : float
        - site : int
        - permeability : float
        - H ind : float
        - isRef : boolean
        - reference_name : string
        - is Steady : boolean
        - simulation_name : string
    """
    
    def __init__(self, approximation, chronicle, rate, site, permeability, isRef, isSteady):
        self.approximation = approximation
        self.chronicle = chronicle
        self.rate = rate
        self.site = site
        self.permeability = permeability
        self.isRef = isRef
        self.isSteady = isSteady


    def create_topo_file(self, folder):
        self.set_simulation_name()
        if folder is None:
            repo = self.get_path_to_simulation_directory()
        else:
            site_name = self.get_site_name_from_site_number()
            repo = folder + "/" + site_name + "/" + self.simulation_name
        topo = self.get_soil_surface_values_for_a_simulation(repo, self.simulation_name)
        np.save(repo + "/soil_surface_topo_"+ self.simulation_name + ".npy", topo)
        print(repo + "/soil_surface_topo_"+ self.simulation_name + ".npy")

    def set_simulation_name(self):
        self.simulation_name = (
            "model_time_0_geo_0_thick_1_K_"
            + str(self.permeability)
            + "_Sy_0.1_Step1_site"
            + str(self.site)
            + "_Chronicle"
            + str(self.chronicle)
        )
        if self.isSteady:
            self.simulation_name += "_SteadyState"
        elif not self.isRef:
            self.simulation_name += "_Approx" + str(self.approximation)
            if self.approximation == 0 or self.approximation == 2:
                self.simulation_name += "_Period" + str(float(self.rate))
            elif self.approximation == 1:
                self.simulation_name += "_RechThreshold" + str(float(self.rate))

    def get_path_to_simulation_directory(self):
        site_name = self.get_site_name_from_site_number()
        return os.path.join("/DATA/These/Projects/modflops/docker-simulation/modflow", "outputs/", site_name, self.simulation_name)


    def get_site_name_from_site_number(self):
        sites = pd.read_csv("/DATA/These/Projects/modflops/docker-simulation/modflow/" + "data/study_sites.txt", sep=",", header=0, index_col=0)  # \\s+
        site_name = sites.index._data[self.site]
        return site_name

    def get_soil_surface_values_for_a_simulation(self, repo_simu, model_name):
        """
            Retrieve the matrix of the topographical altitude.
        """
        mf = flopy.modflow.Modflow.load(repo_simu + "/" + model_name + '.nam')
        dis = flopy.modflow.ModflowDis.load(
            repo_simu + "/" + model_name + '.dis', mf)
        topo = dis.top._array
        return topo

    def get_h_indicator_from_file(self, H_ind_file_path):
        pass



