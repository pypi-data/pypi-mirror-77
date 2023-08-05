import os
import requests
from structure import DownloadPDB, MapUniprotToPDB, PDBtoSequence, CheckDistances
from mapper import GeneToPDB, GeneToUniprot, GeneToFasta

def ObtainActiveCenterResidues(uniprot_id): 

    """
    This function takes an Uniprot ID (str) and returns a list of residue numbers of the active site.
    @ input - uniprot_id (str)
    @ output - ActiveSiteResidues (list)
    """

    response = requests.get("https://www.ebi.ac.uk/thornton-srv/m-csa/api/entries/?entries.proteins.sequences.uniprot_ids=" + uniprot_id)
    json_data = response.json()
    if json_data['results'] == []:
        return None
    return list(map( lambda residue: residue['residue_chains'][0]['resid'], json_data['results'][0]['residues']))


def CheckDistanceToActiveSite(gene, res_number):

    """
    Main function of the package. It takes a GENE ID and a Residue Number and computes the physical distances between the residue to the active site.
    @ input - Gene (str) - Gene identifier
    @ input - res_number (int) - Number of the mutation in Uniprot
    @ output - List of floats: List of distances from res_number to each of the residues of the active site in Amstrongs.
    """

    # Obtain the Active Site residues for the gene.
    ActiveResidues = ObtainActiveCenterResidues(GeneToUniprot(gene))

    if ActiveResidues is None: 
        return "The gene " + gene + " has not an active site mapped in EBI database."

    # Obtain the PDF file
    PDBfile = DownloadPDB(GeneToPDB(gene))

    # Check if the active site residues have structure
    PDB_Residues = MapUniprotToPDB (GeneToFasta(gene), PDBtoSequence(PDBfile), [res_number] + ActiveResidues)
    
    Mutation = PDB_Residues[0]
    PDBActiveSite = PDB_Residues[1:]

    distances = CheckDistances(Mutation, PDBActiveSite, PDBfile)
    os.remove(PDBfile)
    return distances