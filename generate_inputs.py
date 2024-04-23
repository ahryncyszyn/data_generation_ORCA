import argparse
import os

from sample_data import sample_data
from xyz_utils import exportXYZ_with_charge

def generate_inputs(dataset_dir, output_dir, no_batches):
    """ Samples the data from the dataset and creates ORCA input file for each one of them.
    dataset_dir (str): path to the dataset
    output_dir (str): path where to store the results
    no_batches (int): number of batches (molecules per each datatype) to sample
    """

    # create the output directory if it doesn't exist yet
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # sample the data
    # data_points -> list[(coords, atoms, charge, info)]
    elements_all, coords_all, charges_all, names_all = sample_data(dataset_dir, no_batches)
    assert len(coords_all) == len(elements_all) == len(charges_all)
    
    # save sampled data
    os.chdir(output_dir)
    #for i in range(no_molecules):
    for i, (elements, coords, charge, name) in enumerate(zip(elements_all, coords_all, charges_all, names_all)):
        print(f"Saving data for {name}, {coords}, {elements}, charge: {charge}")

        # create a folder for storing calculations of one molecule
        temp_dir_name = f"inp_{i}_{name}"
        temp_dir = os.path.join(output_dir, temp_dir_name)
        os.makedirs(temp_dir)
        os.chdir(temp_dir)

        # create data file with xyz coords
        exportXYZ_with_charge(elements, coords, charge, "molecule.inp")

        # create ORCA input
        ORCA_input_file(elements, coords, charge)
        
    print(f"Input ORCA files have been generated for {len(coords_all)} molecules")



def ORCA_input_file(elements, coords, charge):
    
    with open("molecule.inp", "w") as f:
        f.write("! DLPNO-CCSD(T) cc-pVTZ cc-pVTZ/C TIGHTSCF\n\n")
        f.write("%pal\n")
        f.write("nprocs 8\n")
        f.write("end\n\n")
        f.write("%maxcore 22500\n")
        f.write("%cpcm") 
        f.write("epsilon 80.4") # dielectric constant
        f.write("refrac 1.33") # refractive index
        f.write("rsolv 1.3") # solvent probe radius
        f.write("end")

        #multiplicity set to 2, as all molecules are radicals
        f.write(f"* xyz {charge} 2")

        for element, coord in zip(elements, coords):
            f.write(f"{element.capitalize()} {coord[0]} {coord[1]} {coord[2]}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir')
    parser.add_argument('output_dir')
    parser.add_argument('no_batches')
    args = parser.parse_args()
    generate_inputs(args.dataset_dir, args.output_dir, args.no_batches)
    print("finished generating inputs")
