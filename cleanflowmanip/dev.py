import glob
import os
import re
import pandas as pd
import argparse



path_to_results_folder = "/run/media/jnsll/Seagate Expansion Drive/exps_modflops/results"
path_to_modflops_folder = "/DATA/These/Projects/modflops"

def generate_from_inspection(modflow_folder_path, site_number, chronicle, quality):
    file_names = get_files_in_folder(site_number, chronicle, quality)
    #print(file_names, len(file_names))
    if len(file_names)==30:
        print("All simulations already done! :)")
    else:
        rates_of_existing_files = extract_specs_from_all_file_names(file_names, quality)
        print("Remaining simulations: ", 30 - len(rates_of_existing_files))
        remaining_rates = get_remaining_rates_of_simulations_to_launch(rates_of_existing_files)
        generate_igrida_file_for_remaining_rates_of_a_site(modflow_folder_path, site_number, chronicle, remaining_rates, quality)

def get_files_in_folder(site_number, chronicle, quality):
    site_name = get_site_name_from_site_number(site_number)
    if quality:
        pattern = glob.glob(str(path_to_results_folder) + "/" +  str(site_name)  + "/" + "*/*Chronicle" + str(chronicle) +"*BVE_SUB.csv")
    else:
        pattern = glob.glob(str(path_to_results_folder) + "/" +  str(site_name)  + "/" + "*/*Chronicle" + str(chronicle) +"*.nam")
    files_names = [os.path.basename(x) for x in pattern]
    return files_names


def get_site_name_from_site_number(site_number):
    sites = pd.read_csv(str(path_to_modflops_folder) + "/docker-simulation/modflow/" + "data/study_sites.txt", sep=",", header=0, index_col=0)  # \\s+
    site_name = sites.index._data[site_number]
    return site_name

def extract_specs_from_all_file_names(file_names, quality):
    existing_rates = []
    for file_name in file_names:
        existing_rates.append(extract_spec_from_file_name(file_name, quality))
    return existing_rates

def extract_spec_from_file_name(file_name, quality):
    if quality:
        pattern = r'model_time_0_geo_0_thick_1_K_27.32_Sy_0.1_Step1_site(\d+)_Chronicle(\d+)(?:_Approx(\d)_Period(\d+).0)?_Ref_model_time_0_geo_0_thick_1_K_27.32_Sy_0.1_Step1_site\d+_Chronicle\d+_errorsresult_H_BVE_SUB.csv'
    else:        
        pattern = r'model_time_0_geo_0_thick_1_K_27.32_Sy_0.1_Step1_site(\d+)_Chronicle(\d+)(?:_Approx(\d)_Period(\d+).0)?.nam'
    m = re.search(pattern, file_name)
    if m is None:
        print("Does not match the pattern to extract info from filename '" + str(file_name) + "'.")
        return
    else:
        site_number = m.group(1)
        chronicle = m.group(2)
        approx = m.group(3)
        rate = m.group(4)
        if approx is None and rate is None:
            return 0
        else:
            return int(rate)


def get_remaining_rates_of_simulations_to_launch(rates_of_existing_files):
    rates = [0, 2, 7, 15, 21, 30, 45, 50, 60, 75, 90, 100, 125, 150, 182, 200, 250, 300, 330, 365, 550, 640, 730, 1000, 1500, 2000, 2250, 3000, 3182, 3652]
    remaining_rates = list(set(rates).symmetric_difference(set(rates_of_existing_files)))
    return remaining_rates

def generate_igrida_file_for_remaining_rates_of_a_site(modflow_folder_path, site_number, chronicle, remaining_rates, quality):
    if quality:
        file_name = modflow_folder_path + "/scripts/" + 'params_site' + str(site_number) + "_chr" + str(chronicle) + "_giec" + '_remaining_H.txt'
    else:
        file_name = modflow_folder_path + "/scripts/" + 'params_site' + str(site_number) + "_chr" + str(chronicle) + "_giec" + '_remaining.txt'
    with open(file_name, 'w') as f:
        for rate in remaining_rates:
            if rate == 0:
                f.write("%s %s %s %s %s %s %s %s %s\n" % (site_number, chronicle, 0, rate, 1, 27.32, 0, 0, 0))
            else:
                f.write("%s %s %s %s %s %s %s %s %s\n" % (site_number, chronicle, 0, rate, 0, 27.32, 0, 0, 0))
    print("File: ", file_name, " created!")




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-chr", "--chronicle", type=int, required=True)
    parser.add_argument("-site", "--sitenumber", type=int, required=True)
    parser.add_argument("-quality", "--quality", action='store_true')
    args = parser.parse_args()

    chronicle = args.chronicle
    site_number = args.sitenumber
    quality = args.quality

    generate_from_inspection(path_to_modflops_folder, site_number, chronicle, quality)