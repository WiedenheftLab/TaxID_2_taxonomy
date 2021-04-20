#!/usr/venv/bin/python

import argparse
import sys
import subprocess
import os
import distutils.spawn
import textwrap

try:
    import tqdm
except ImportError, e:
    print "tqdm module is not installed! Please install tqdm and try again."
    sys.exit()

if (distutils.spawn.find_executable("efetch")) == None:
    print("\nERROR: efetch is not installed. Please make sure NCBI Entrez tools are defined in path.\n")
    sys.exit()

parser = argparse.ArgumentParser(prog='python TaxID_2_taxonomy.py',
      formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\

      	Author: Murat Buyukyoruk
      	Associated lab: Wiedenheft lab

        TaxID_2_taxonomy help:

This script is developed to assign taxonomy by using the TaxID of genomes, which can be fetched from NCBI database

NCBI Entrez package is required to fetch taxonomy (efetch). Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        
Syntax:

        python TaxID_2_taxonomy.py -i demo_taxID.txt -o demo_taxonomy.txt

TaxID_2_taxonomy dependencies:
	NCBI Entrez                         refer to https://www.ncbi.nlm.nih.gov/books/NBK179288/
	tqdm                                refer to https://pypi.org/project/tqdm/
	
Input Paramaters (REQUIRED):
----------------------------
	-i/--input		List			Specify file name contains the list of TaxID in each row.

	-o/--output		Dataframe		Specify a output file name that will contain the Taxonomy information.

Basic Options:
--------------
	-h/--help		HELP			Shows this help text and exits the run.
	
      	'''))
parser.add_argument('-i', '--input', required=True, type=str, dest='filename', help='Specify a fastafile.\n')
parser.add_argument('-o', '--output', required=True, dest='out',
                    help='Specify a output file name.\n')

orig_stdout = sys.stdout

results = parser.parse_args()
filename = results.filename
out = results.out

os.system('> ' + out)

proc = subprocess.Popen("wc -l < " + filename, shell=True, stdout=subprocess.PIPE, )
length = int(proc.communicate()[0].split('\n')[0])

f = open(out, 'a')
sys.stdout = f

print "taxID\tkingdom\tphylum\tclass"

with tqdm.tqdm(range(length), desc='Fetching...') as pbar:
    with open(filename,'rU') as file:
        for line in file:
            pbar.update()
            if "taxaid" not in line:
                try:
                    line.split()[0]
                    taxID = line.split()[0]
                    kingdom = line.split()[1]
                    phylum = line.split()[2]
                    class_old = line.split()[3].split('\n')[0]
                except:
                    taxID = line.split('\n')[0]
                    kingdom = "NA"
                    phylum = "NA"
                    class_old = "NA"
                if kingdom == "NA" or phylum == "NA" or class_old == "NA":
                    proc = subprocess.Popen('efetch -db taxonomy -id '+ taxID + ' -format xml | xtract -pattern Taxon -first TaxId -element Taxon -block "*/Taxon"  -unless Rank -equals "no rank" -tab "\n" -sep "_" -element Rank,ScientificName |grep "superkingdom" | cut -d"_" -f2', shell=True, stdout=subprocess.PIPE, )
                    kingdom_new = (proc.communicate()[0].split('\n')[0])

                    proc = subprocess.Popen('efetch -db taxonomy -id '+ taxID + ' -format xml | xtract -pattern Taxon -first TaxId -element Taxon -block "*/Taxon"  -unless Rank -equals "no rank" -tab "\n" -sep "_" -element Rank,ScientificName |grep "phylum" | cut -d"_" -f2', shell=True, stdout=subprocess.PIPE, )
                    phylum_new = (proc.communicate()[0].split('\n')[0])

                    proc = subprocess.Popen('efetch -db taxonomy -id '+ taxID + ' -format xml | xtract -pattern Taxon -first TaxId -element Taxon -block "*/Taxon"  -unless Rank -equals "no rank" -tab "\n" -sep "_" -element Rank,ScientificName |grep "class" | cut -d"_" -f2', shell=True, stdout=subprocess.PIPE, )
                    class_new = (proc.communicate()[0].split('\n')[0])

                    print taxID + '\t' + kingdom_new + '\t' + phylum_new + '\t' + class_new

                else:
                    print line.split('\n')[0]
