import re
import sys

from Parser.NCBI import *
from Parser.KEGG import KEGG_parse
from Parser.Ensembl import ensembl_parse
from Parser.Uniprot import uniprot_parse
from Parser.PDB import pdb_parse
from Parser.String import string_parse
from Parser.GOterm import go_parse
from Parser.Prosite import Prosite_parse
from Parser.PFAM import PFAM_parse

def result_writer():
	relative_path = sys.path[0]
	output_file = open(relative_path + '/result.html', 'w')
	begin_file = open(relative_path + '/begin_template.html', 'r')
	output_file.write(begin_file.read())
	begin_file.close()

	gene_analyser(output_file)

	end_file = open(relative_path + '/end_template.html', 'r')
	output_file.write(end_file.read())
	end_file.close()
	output_file.close()

def gene_analyser(output_file):
	gene_file = open(sys.argv[1], 'r')
	gene_line = gene_file.read().splitlines()
	list_go_type = ['biological_process', 'molecular_function', 'cellular_component']

	for line in gene_line:
		if line != "":
			list_line = line.split('\t')
			clean_org = re.sub("(\s)$", "", list_line[1])
			print(list_line)
			output_file.write('<tr>\n')
			output_file.write('<td><div class=\"Expander\"><img src="https://img.icons8.com/color/48/000000/plus.png" onclick="this.src = this.src == minusImg ? plusImg : minusImg;"></div></td>')
			output_file.write('<td><div class=\"collapse\">' + list_line[0].upper() + '</div></td>\n<td><div class=\"collapse\">' + clean_org + '</div></td>\n')
			org_no_space = re.sub("(\s)", "_", clean_org)
			lower_org_no_space = org_no_space.lower()

			list_gene_id = Gene_parse(list_line[0], lower_org_no_space, output_file)
			Refseq_parse("nucleotide", "M", lower_org_no_space, list_line[0], output_file)
			Refseq_parse("protein", "P", lower_org_no_space, list_line[0], output_file)
			KEGG_parse(list_gene_id, output_file)

			ensembl_parse(list_line[0], lower_org_no_space, output_file)

			uniprot_list = uniprot_parse(list_line[0], lower_org_no_space, output_file)
			for go_type in list_go_type:
				go_parse(uniprot_list, go_type, output_file)
			pdb_parse(uniprot_list, output_file)
			string_parse(uniprot_list, output_file)
			Prosite_parse(uniprot_list, output_file)
			PFAM_parse(uniprot_list, output_file)
			output_file.write('</tr>\n')
			print("===========================================\n")


result_writer()

