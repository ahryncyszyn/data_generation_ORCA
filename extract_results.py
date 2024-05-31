
import numpy as np
import argparse
import os

def extract_results(calculations_path, results_path):
    """ Extracts the total energy from each ".out" ORCA file. Creates two files:
    "data.xyz" - containing all of the molecules in xyz format
    "labels.npy" - containing all of the corresponding energies in the same order

    calculations_path (str): path to the folder created by "inputs_generation.py", 
                         contains all calculations and their results
    results_path (str): path where the results will be saved
    """

    # find paths to all of the calculations
    mol_paths = [os.path.join(calculations_path, path) for path in os.listdir(calculations_path)]

    # create results files
    data_file = open(os.path.join(results_path, 'data_molecules.xyz'), 'a')
    energies_file = os.path.join(results_path, 'labels.npy')

    # append all results to results files
    for mol_path in mol_paths:
        os.chdir(mol_path)

        # read out and append the energy value
        with open('molecule.out') as f:
            for line in f:
                words = line.strip().split()
                if len(words) == 5 and words[0:4] == ['FINAL', 'SINGLE', 'POINT', 'ENERGY']:
                    energy = float(words[4])
                    break

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

    data_file.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('calculations_path')
    parser.add_argument('results_path')
    args = parser.parse_args()

    extract_results(args.calculations_path, args.results_path)
    print("finished extracting data")

