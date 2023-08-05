import os
import sys

import numpy as np
import pandas as pd
from collections import Counter

from pymatgen import Structure, Element
from scripts.files import vaspname

def rotation(the, ph, ps):
    theta = np.radians(the)
    phi = np.radians(ph)
    psi = np.radians(ps)
    ct, st = np.cos(theta), np.sin(theta)
    cph, sph = np.cos(phi), np.sin(phi)
    cps, sps = np.cos(psi), np.sin(psi)
    R = np.array(((ct*cps, -ct*sps, st), (sph*st*cps+cph*sps, -sph*st*sps +cph*cps, -sph*ct), (-cph*st*cps+sph*sps, cph*st*sps+sph*cps, cph*ct)))
    return R

class Molecule:
    def _loadmolecule(name):
        path = "%s/zero_coords"%(os.path.split(__file__)[0])
        if name == "MA":
            ms = Structure.from_file("%s/MA.json"%(path))
        elif name == "FA":
            ms = Structure.from_file("%s/FA.json"%(path))
        return ms

    def _selective_bool(species, type_num):
        length = len(species)
        if type_num == 1:
            sp = [[True, True, True] for i in range(length)]
        elif type_num == 2:
            sp = [[False, False, False] for i in range(length)]
        elif type_num == 3:
            sp = []
            for i in range(length):
                if species[i].symbol in ["H", "C", "N"]:
                    sp.append([False, False, False])
                else:
                    sp.append([True, True, True])
        elif type_num == 4:
            sp = []
            for i in range(length):
                if species[i].symbol in ["H", "C", "N"]:
                    sp.append([True, True, True])
                else:
                    sp.append([False, False, False])
        return sp
    
    def __init__(self, random_coord=True, random_degree=True):
        self.random_coord = random_coord
        self.random_degree = random_degree
        if self.random_coord == False and self.random_degree == False :
            if os.path.isfile("%s/MOLE"%(os.getcwd())) :
                rmole = open("%s/MOLE"%(os.getcwd()),"r").readlines()
                self.cord = [int(i.split()[0]) for i in rmole]
                self.degree = [list(map(int,i.split()[1:])) for i in rmole]
            else :
                print("Please make the 'MOLE' file!\n")
                sys.exit(0)
        elif self.random_coord == False and self.random_degree == True :
            if os.path.isfile("%s/MOLE"%(os.getcwd())) :
                rmole = open("%s/MOLE"%(os.getcwd()),"r").readlines()
                print(rmole)
                self.cord = [int(i.split()[0]) for i in rmole]
                self.degree = None
            else :
                print("Please make the 'MOLE' file!\n")
                sys.exit(0)
        else :
            self.cord = None
            self.degree = None

    def _inputinform(self):
        while True :
            inputatom = str(input("Enter the elements >> "))
            try :
                Element(inputatom)
                break
            except :
                print("\nThere is no %s in structure\nPlease one more enter\n"%(inputatom))
        if self.cord != None :
            change = 1
        else :
            change = float(input("Enter the change ratio(ex.0.7) >> "))
            if change > 1 :
                change = 1

        while True :
            inputfix = str(input("Do you want to apply selective dynamic?(Y or N) >> "))
            if inputfix == "Y":
                print("\n#########################################################################################################")
                print("#\t1. Do you want to apply T to all elements? Please enter 1\t\t\t\t\t#")
                print("#\t2. Do you want to apply F to all elements? Please enter 2\t\t\t\t\t#")
                print("#\t3. Do you want to apply T to the inorganic element and F to the organic element? Please enter 3 #")
                print("#\t4. Do you want to apply F to the inorganic element and T to the organic element? Please enter 4 #")
                print("#########################################################################################################\n")
                while True :
                    fixcalc = int(input("Please refer to the options above >> "))
                    if fixcalc in [1,2,3,4]:
                        break
                    else :
                        print("There isn't in option")
                break
            elif inputfix == "N" :
                fixcalc = None
                break
            else :
                print("Please enter the Y or N\n")
        if self.random_coord == False and self.random_degree == False :
            multiple = 1
        elif self.random_coord == True and self.random_degree == False :
            self.degree = np.array(list(map(int,input("Please enter the degree >> ").split())))
            multiple = int(input("Enter the number of the times to repeat >> "))
        else :
            multiple = int(input("Enter the number of the times to repeat >> "))
        return inputatom, change, fixcalc, multiple

    def tiltingmolecule(self, s, ms, inputatom, changenum, fixcalc=None):
        s_matrix = s.lattice.matrix
        s_species = s.species
        ms_species = ms.species
        s_coord = np.dot(s.frac_coords, s_matrix).tolist()
        ms_coord = np.dot(ms.frac_coords, ms.lattice.matrix)
        name = vaspname(s)
        # pick the index of inputatom and shuffle 
        s_index = np.array([e for e,c in enumerate(s_species) if c.symbol == Element(inputatom).symbol])
        if self.random_coord :
            np.random.shuffle(s_index)
            self.cord = s_index[:round(changenum*len(s_index))]
        else :
            for r in self.cord :
                if not r in s_index :
                    print("%i isn't %s index\nPlease revise the index number\n" % (r, inputatom))
                    sys.exit(0)
        r_coord = [s_coord[f] for f in self.cord]

        # make array of degree 
        if self.random_degree :
            self.degree = np.random.randint(360, size=(len(r_coord),3))
            new_ = self.degree
        else :
            if not self.random_coord :
                self.degree = np.array(self.degree)
                new_ = self.degree
            else:
                new_ = [[self.degree[0], self.degree[1], self.degree[2]] for i in range(len(r_coord))]
        # add coordination
        lthe=[];lph=[];lps=[]
        for coord, degree in zip(r_coord,new_):
            index = s_coord.index(coord)
            del s_coord[index]
            del s_species[index]

            the, ph, ps = degree[0], degree[1], degree[2]
            lthe.append(degree[0])
            lph.append(degree[1])
            lps.append(degree[2])
            R = rotation(the, ph, ps)
            dot = np.dot(ms_coord, R)
            s_coord.extend(np.add(dot, coord).tolist())
            s_species.extend(ms_species)
        # csv 
        df = pd.DataFrame({'index':self.cord,'Theta':lthe,'Phi':lph,'Psi':lps})
        df.set_index('index')

        # add the properties of selective_dynamics 
        if fixcalc != None :
            sp = Molecule._selective_bool(species=s_species, type_num=fixcalc)
            new_s = Structure(s_matrix, s_species, s_coord, coords_are_cartesian=True,site_properties={"selective_dynamics":sp})
        else :
            new_s = Structure(s_matrix, s_species, s_coord, coords_are_cartesian=True)
        new_s.sort()
        return new_s, df

def analyze_mole(args) :
    if args.ma :
        mafa = "MA"
    elif args.fa :
        mafa = "FA"
    ms = Molecule._loadmolecule(mafa)
    
    pwd = os.getcwd()
    cur = pwd.split(os.path.sep)[-1]
    file_ = os.path.abspath(args.name[0])
    filename = os.path.basename(file_)

    mole = Molecule(random_coord=args.position, random_degree=args.degree)
    inputatom, changenum, fixcalc, multiple = mole._inputinform()

    # naming 
    if fixcalc == None :
        cur1 = "%s_ration%.2f%%_multiple%i_from_%s_%s"%(cur,changenum*100,multiple,filename,mafa)
    else :
        cur1 = "%s_ration%.2f%%_multiple%i_selective%i_from_%s_%s"%(cur,(changenum*100),multiple,fixcalc,filename,mafa)

    if os.path.isfile(file_):
        s = Structure.from_file(file_)
        vaspname_ = vaspname(s)
        for i in range(multiple):
            m = mole.tiltingmolecule(s, ms, inputatom=inputatom, changenum=changenum,
            fixcalc = fixcalc)
            m[0].to(filename="POSCAR_%s_multiple%i"%(vaspname_,i+1))
            if args.csv :
                m[1].to_csv("%s_%i.csv"%(vaspname_,i+1))

    else :
        filesum=0
        for j in os.listdir(file_):
            try :
                s = Structure.from_file("%s/%s"%(file_,j))
                vaspname_ = vaspname(s)
                for i in range(multiple):
                    m = mole.tiltingmolecule(s, ms, inputatom=inputatom, changenum=changenum,fixcalc = fixcalc)
                    m[0].to(filename="POSCAR_%s_multiple%i"%(vaspname_,filesum+1))
                    if args.csv :
                        m[1].to_csv("%s_%i.csv"%(vaspname_,filesum+1))
            except :
                pass
    os.makedirs(os.path.join(cur1),exist_ok=True)
    os.system("mv %s/POSCAR_*_multiple* %s/%s"%(pwd,pwd,cur1))
    if args.csv :
        os.system("mv %s/*.csv %s/%s"%(pwd,pwd,cur1))
    print("Generate %s/%s"%(pwd,cur1))
