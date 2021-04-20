# TaxID_2_taxonomy

Author: Murat Buyukyoruk

Associated lab: Wiedenheft lab

# TaxID_2_taxonomy help:

This script is developed to assign taxonomy by using the TaxID of genomes, which can be fetched from NCBI database

NCBI Entrez package is required to fetch taxonomy (efetch). Additionally, tqdm is required to provide a progress bar since some multifasta files can contain long and many sequences.
        
Syntax:

        python TaxID_2_taxonomy.py -i demo_taxID.txt -o demo_taxonomy.fasta

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
  
# Note:
Demo files are available to use with the basic command line provided in syntax section above. Make sure all the dependencies are installed successfully to the python environment.

      demo_taxID.txt          Includes list of TaxIDs
