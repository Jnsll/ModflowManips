"""Main module."""

from File import H5File 

f = H5File("test_June_IPS1_Cell_1_RCP4-5.h5", r"/run/media/jnsll/Seagate Expansion Drive/SURFEX_OSUR/SURFEX/OUT", "IPS1", "RCP4.5", "REC", 1)

f.retrieve_data()
f.format_data()

data = f.get_formatted_data()
print(data)
f.store_formatted_data_into_txt_file()