"""Main module."""

from File import H5File 

for scenario in ["RCP2.6", "RCP4.5", "RCP8.5"]: 
    for cell in [1, 888, 2108, 5021, 7288, 8510]:

        f = H5File(r"/run/media/jnsll/Seagate Expansion Drive/SURFEX_OSUR/SURFEX/OUT", "IPS1", scenario, "REC", cell)

        f.retrieve_data()
        f.format_data()

        data = f.get_formatted_data()
        f.store_formatted_data_into_txt_file()