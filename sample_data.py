import pandas as pd
import random
import os
import re
from xyz_utils import readXYZs, find_mol_charge

def sample_data(xyz_files_dir, no_batches):
    
    # list all of the datatypes in dataset directory
    all_items = os.listdir(xyz_files_dir)
    datatypes_paths = [os.path.join(xyz_files_dir, item) for item in all_items 
                      if os.path.isdir(os.path.join(xyz_files_dir, item))]
    print(f"Found datatypes are {datatypes_paths}")

    # initialize variables for the data sampling
    coords_all, elements_all, charges_all, names_all = [], [], [], []
    working_dir = os.getcwd()

    # sample data for each datatype
    for datatype_path in enumerate(datatypes_paths):

        # go into the folder containing certain data type and list all files inside
        os.chdir(datatype_path)
        all_files = os.listdir()

        # find the xyz and info file based on the normal expression (adjust in case of a different dataset!)
        file_pattern_coords = r'.*se1_ID_0_coords.xyz$' 
        file_pattern_info = r'.*se1_ID_0_info.csv$'         #change to se3 if necessary
        pattern_coords = re.compile(file_pattern_coords)
        pattern_info = re.compile(file_pattern_info)

        # read the coordinates and elements from the xyz file
        coords_file = [file for file in all_files if pattern_coords.match(file)][0]
        print(f"sampling data from data type {coords_file}")
        coords_dataset_1type, elements_dataset_1type = readXYZs(coords_file)
        assert len(coords_all) == len(elements_all)
        
        # read names of molecules from the info file
        info_file_path = [file for file in all_files if pattern_info.match(file)][0]
        info_df = pd.read_csv(info_file_path, usecols=['names'])
        system_names = info_df['names'].tolist()
        
        # sample random molecules (indices)
        num_dataset_molecules = len(coords_dataset_1type)
        sampled_indices = random.sample(range(num_dataset_molecules), no_batches)

        # save the data of sampled molecules
        coords_sampled = [coords_dataset_1type[i] for i in sampled_indices]
        elements_sampled = [elements_dataset_1type[i] for i in sampled_indices]
        charges_sampled = [find_mol_charge(i, system_names) for i in sampled_indices]
        names_sampled = [system_names[i] for i in sampled_indices]

        # append the info to all sampled molecules for flavour
        coords_all.extend(coords_sampled)
        elements_all.extend(elements_sampled)
        charges_all.extend(charges_sampled)
        names_all.extend(names_sampled)

        # go back to the dataset directory
        os.chdir(working_dir)

    return elements_all, coords_all, charges_all, names_all
