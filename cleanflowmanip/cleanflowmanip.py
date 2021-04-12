"""Main module."""

from File import H5File 
from File import SimuInputFile

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