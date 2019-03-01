# M1 Bioinformatics Project

## Tutorial
The Python scrypt called main.py run an analysis of the gene_symbols associated with an organism. From these data,some databases are requested. Firstly the NCBI database , where the NCBI ID is recovered... Then the Ensembl database to recover the gene ID, the transcripts IDs, the protein IDs, the list of orthlogs and then a link to a genome browser. Finally Uniprot is requested to get the Uniprot IDs and the protein name. With the Uniprot ID 3 databases are requested. Firstly, Go is requested three times to get the biological process, the molecular function and the cellular component. Then, PDB is request to get the Structure name and ID. Finally The Uniprot ID is used to create a link to a STRING image which represent the interaction map. 

All the result are available in the html table.

The data available in this table are :
 - The Gene symbol
 - The specie
 - The NCBI ID
 - The Ensembl Gene ID
 - The Ensembl Transcript IDs
 - The Ensembl Protein IDs
 - The Uniprot IDs
 - The Go Terms
   - The Biological Process
   - The Molecular Function
   - The Cellular Component
 - The PDB Ids with Structure Names
 - The String Interaction Maps
 
## Files explanation
