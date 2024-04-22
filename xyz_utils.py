
def readXYZs(coords_file):
    ''' Reads multiple molecules from a xyz file. '''

    coords = []
    elements = []

    with open(coords_file, "r") as f:
        for line in f:
            words = line.split()

            if len(words) == 1 and words[0].isnumeric():
                coords.append([])
                elements.append([])
            elif len(words) == 4:
                split_line = line.split()
                elements[-1].append(split_line[0].capitalize())
                coords[-1].append([float(split_line[1]), float(split_line[2]), float(split_line[3])])

    return coords, elements


def find_mol_charge(i, system_names):
    ''' Determines the charge of the molecule based on its name containing + or - signs

    i (int): index of the molecule to be calculated
    system_names (list): list of names of the molecules from the info csv file
    '''
    system = system_names[i]
    pos_chr = system.count('+')
    neg_chr = system.count('-')
    tot_chr = pos_chr - neg_chr   

    return tot_chr


def exportXYZ_with_charge(elements, coords, charge, filename):
    ''' Saves the information about molecule in one xyz file containing charge value next to the atoms count'''

    with open(filename, "w") as f:
        f.write(f"{len(coords)} {charge}\n")

        assert len(elements) == len(coords)
        for element, coord in zip(elements, coords):
            f.write(f"{element.capitalize()} {coord[0]} {coord[1]} {coord[2]}\n")

    