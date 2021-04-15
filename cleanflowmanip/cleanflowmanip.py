"""Main module."""

from File import H5File 
from File import SimuInputFile
from File import ChronicleCriteriaFile
from File import IgridaParamsLaunchFile

# # Create reference files from surfex h5 files
# for scenario in ["RCP2.6", "RCP4.5", "RCP8.5"]: 
#     for cell in [1, 888, 2108, 5021, 7288, 8510]:

#         f = H5File(r"/run/media/jnsll/Seagate Expansion Drive/SURFEX_OSUR/SURFEX/OUT", "IPS1", scenario, "REC", cell)

#         f.retrieve_data()
#         f.format_data()

#         #data = f.get_formatted_data()
#         f.store_formatted_data_into_reference_file()

# # Create an custom input file
# simu = SimuInputFile(0, 27, False, 18)
# simu.set_modflow_app_folder_path(r"/DATA/These/Projects/modflops/docker-simulation/modflow")
# simu.generate_custom_input_file()


# chronicle_crits = ChronicleCriteriaFile("/DATA/These/Projects/LAPrediction", range(10, 28))
# chronicle_crits.create_chronicle_file()


for site_number in range(1, 15):
    launch_file = IgridaParamsLaunchFile(site_number, None, 0, 27.32)
    launch_file.set_modflow_app_folder_path(r"/DATA/These/Projects/modflops")
    launch_file.generate_giec_file_for_a_site()
