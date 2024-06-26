
import numpy as np
import argparse
import shutil
import os

def extract_results(data_path, results_path, storage_path):
    """ Extracts the total energy from each ".out" ORCA file. Creates two files:
    "data_molecules.xyz" - containing all of the molecules in xyz format
    "final_energies.npy" - containing all of the corresponding energies in the same order

    data_path (str): path to the folder created by "inputs_generation.py", 
                    contains all calculations and their results in separate folders
    results_path (str): path where the results will be saved
    storage_path (str): path where the calculations data will be moved at the end for storage
    """
    # for units conversion Hartree --> eV
    HToeV = 27.211399

    # find paths to all of the calculations
    mol_paths = [os.path.join(data_path, path) for path in os.listdir(data_path)]

    # create results files or open existing ones
    data_file = open(os.path.join(results_path, 'data_molecules.xyz'), 'a')
    energies_file = os.path.join(results_path, 'final_energies.npy')

    # append all results to results files
    for mol_path in mol_paths:
        os.chdir(mol_path)

        # read out the energy value and convert it to eV
        with open('molecule.out') as f:
            energy = None
            for line in f:
                words = line.strip().split()
                if len(words) == 5 and words[0:4] == ['FINAL', 'SINGLE', 'POINT', 'ENERGY']:
                    energy = float(words[4]) * HToeV
                    break

        # skip this molecule if the calculation did not converge        
        if energy is None:
            print(f"missing result of calculation {mol_path}")
            continue

        # append the energy to results
        if os.path.exists(energies_file):
            all_energies = np.load(energies_file)
        else:
            all_energies = np.array([])
        energies = np.concatenate((all_energies, np.array([energy])))
        np.save(energies_file, energies)

        # append the xyz data
        with open('data.xyz') as f:
            for line in f:
                data_file.write(line)
        data_file.write('\n')
        shutil.move(mol_path, storage_path)

    data_file.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path')
    parser.add_argument('results_path')
    parser.add_argument('storage_path')
    args = parser.parse_args()

    extract_results(args.data_path, args.results_path, args.storage_path)
    print("finished extracting data")

