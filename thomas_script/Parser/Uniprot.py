import requests
import re


def uniprot_parse (gene_symbol, organism, output_file):
	'''
	:param gene_symbol:
	:param organism:
	:param output_file:
	:return: the list of Uniprot ID
	Write the Uniprot ID and the protein name in the output file
	'''
	url = "http://www.uniprot.org/uniprot/"
	acc_list = []
	print("Querying Uniprot...")
	payload = {
		'query': 'gene_exact:' + gene_symbol + ' AND organism:' + organism + ' AND fragment:no',
		'format': 'tab',
		'columns': 'id,protein_names',
		}
	result = requests.get(url, params=payload)
	if result.ok:
		if result.text:
			uniprot_data = result.text.split('\n')  # Change the tab text into list
			del uniprot_data[0]  # Remove the first elem which is the column names
			output_file.write('<td><div class=\"collapse\">')
			for data in uniprot_data[:-1]: # read list without the last line which is a blank line
				data_list = data.split('\t')  # split the elem with the ID in the first position
				output_file.write('<a href="{0}{1}">{1}</a><br>'.format(url, data_list[0]))
				acc_list.append(data_list[0])  # Create the Uniprot ID list
			output_file.write('</div></td>\n')
			output_file.write('<td><div class=\"collapse\">')
			for data in uniprot_data[:-1]: # read list without the last line which is a blank line
				data_list = data.split('\t')  # split the elem with the ID in the second position
				prot_name = re.sub('( [\(|\[].*[\)|\]])', '', data_list[1])  # remove the other names inside parenthesis or bracket
				if prot_name:  # Check if the Name still exist
					output_file.write(prot_name + '<br>\n')
			output_file.write('</div></td>\n')

		else:
			output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
			output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
	else:
		output_file.write('<td><div class=\"collapse\"> Uniprot Not Available </div></td>\n')
		output_file.write('<td><div class=\"collapse\"> Uniprot Not Available </div></td>\n')
	return acc_list
