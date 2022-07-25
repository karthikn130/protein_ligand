## Usage: python combine_gro.py protein.gro jz4.gro 
import sys
import os 

def getNumProtligand_name(fl):
    nres = int(fl[0:5])
    return(nres+1)

def WriteComplexGro(protein_data,ligand_data):
    ofile=open('complex.gro','w')
    ofile.write('%s\n'%protein_data[0])
    ofile.write('%5d\n'%tot_num)
    for line in protein_data[2:-1]: ofile.write('%s\n'%line)
    for line in ligand_data[2:-1]: ofile.write('%s\n'%('%5d'%res_num+line[5:]))
    ofile.write('%s\n'%protein_data[-1])
    ofile.close()
    return None

def editTopologyFile(ligand_name):
    topol = open('topol.top','r').readlines()
    olines = []
    count = 0
    for line in topol: 
        olines.append(line)
        if 'forcefield.itp' in line:
            olines.append(';include ligand dihedral parameters\n')
            olines.append('#include \"%s.prm\"'%ligand_name)
        if 'posre.itp' in line: 
            count = count+1
        if 'endif' in line: 
            if count == 1:
                olines.append('#include \"%s.itp\"'%ligand_name)
                count = 0

    olines.append('%-15s     1\n'%ligand_name)
    ofile = open('topology.top','w')
    for line in olines: ofile.write('%s'%line)
    return None 

protein_gro = sys.argv[1]
ligand_gro = sys.argv[2]

def getFileName(file_name):
    return file_name.split('.')[0]

ligand_gro_noext = getFileName(ligand_gro)

pro = open(protein_gro,'r').readlines()
lig = open(ligand_gro,'r').readlines()

protein_data = [line.rstrip() for line in pro]
ligand_data = [line.rstrip() for line in lig]

res_num = getNumProtligand_name(protein_data[-2])
tot_num = int(protein_data[1])+int(ligand_data[1])

## Write Protein-Ligand Complex GRO file 
WriteComplexGro(protein_data,ligand_data)

## Edit topol.top to add ligand part 
editTopologyFile(ligand_gro_noext)


# rename a file to a new name
def rename_file(file_name,new_name):
    os.rename(file_name,new_name)
    return None

# backup topol file
rename_file('topol.top','topology_backup.top')
rename_file('topology.top','topol.top')

