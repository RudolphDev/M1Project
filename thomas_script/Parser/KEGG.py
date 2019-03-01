import requests
import re


def KEGG_parse(list_id, output_file):
    '''
    :param list_id: from Gene NCBI
    :param output_file:
    :Write the Kegg ID and pathway in the result file
    '''
    print("Querying KEGG...")
    string_id = "+".join(list_id)  # Create a string with all the Ids
    url = "http://rest.kegg.jp/conv/genes/ncbi-geneid:{}".format(string_id)
    kegg_url = "https://www.genome.jp/dbget-bin/www_bget?"
    pathway_url = "https://www.genome.jp/kegg-bin/show_pathway?"
    response = requests.get(url)
    if response.ok:
        kegg = response.text.rstrip()
        list_temp = kegg.split("\t")  # Split the result into list with the kegg id at the second position
        list_kegg = list_temp[1::2]  # Get only the second element which is the kegg id
        if len(list_kegg) != 0:  # Check if the list is not empty
            output_file.write("<td><div class=\"collapse\">")
            for kegg_id in list_kegg:  # Write all id in the file
                output_file.write("<a href=\"{0}{1}\">{1}</a><br>\n".format(kegg_url, kegg_id))
            output_file.write("</div></td>\n")

            output_file.write("<td><div class=\"collapse\">")
            for kegg_id in list_kegg:  # Write all the pathway for each kegg id
                url_path = "http://rest.kegg.jp/get/+{}".format(kegg_id)
                response = requests.get(url_path)
                if response.ok:
                    letters = kegg_id[:3] # Get the three letters from the specie
                    regex_path = " (" + letters + "\d{5})  (.*)" # Regex to get path id and name from the text file
                    list_id_name = re.findall(regex_path, response.text)
                    if len(list_id_name) != 0:
                        for id_name in list_id_name:
                            output_file.write("<a href=\"{0}{1}\">{1} : {2}</a><br>\n".format(pathway_url, id_name[0], id_name[1]))
                    else:
                        output_file.write("No Data Available")
            output_file.write("</div></td>\n")
        else:
            output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
            output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
    else:
        output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
        output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')

