import requests
import re


def pdb_parse(uniprot_list, output_file):
    """
    :param uniprot_list:
    :param output_file:
    :return: Write the result from PDB request thanks to the Uniprot List
    """
    if len(uniprot_list) != 0:
        url = 'http://www.rcsb.org/pdb/rest/search'
        final_url = 'https://www.rcsb.org/structure/'
        uniprot_string = ','.join(uniprot_list)  # Create the string with all the accession
        query_text = """
        <orgPdbQuery>
        <queryType>org.pdb.query.simple.UpAccessionIdQuery</queryType>
        <accessionIdList>""" + uniprot_string + """</accessionIdList>
        </orgPdbQuery>
        """

        print("querying PDB...")

        header = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(url, data=query_text, headers=header)

        if response.ok:  # Check if the query was ok and the website answer
            if response.text != "null\n":  # Check if result not null
                output_file.write("<td><div class=\"collapse\">")
                list_id = re.sub('\n', ',', response.text[:-1])  # Create a string with all the PDB ID
                clean_list_id = re.sub('(:\d+)', '', list_id)
                id_struct = requests.get("""http://www.rcsb.org/pdb/rest/customReport.csv?pdbids=""" + clean_list_id +
                                         """&customReportColumns=structureId,structureTitle,&format=csv""")
                # Get All The structure title form the PDB ID
                list_id_struct = id_struct.text.split("<br />")
                del list_id_struct[0]  # Delete the header
                del list_id_struct[len(list_id_struct)-1]  # delete the last empty line
                for id_struct in list_id_struct:  # Parse the list to get the ID and the structure
                    pdb_list = id_struct.split(',')  # Split to separate the ID and the structure
                    id = pdb_list[0]
                    clean_id = re.sub('\"', '', id)  # Delete the quotes
                    structure = pdb_list[1]
                    clean_structure = re.sub('\"', '', structure) # Delete the quotes
                    output_file.write('<a href="{0}{1}">{1} : {2}</a><br>\n'.format(final_url, clean_id, clean_structure))

                output_file.write('</div></td>\n')
            else:
                output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
        else:
            output_file.write("<td><div class=\"collapse\"> PDB not Available </div></td>\n")
    else:
        output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')


