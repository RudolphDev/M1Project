import requests
import re


def PFAM_parse(uniprot_list, output_file):
    '''
    :param uniprot_list:
    :param output_file:
    :write: the PFAM information
    '''
    print("Querying PFAM...")
    if len(uniprot_list) != 0:  # Check if the list is not empty
        output_file.write("<td><div class=\"collapse\">")
        pfam_url = "https://pfam.xfam.org/protein/"
        for uni_id in uniprot_list: # For each uniprot ID write a viewer icon and domain list
            output_file.write('<a href="{0}{1}">Protein {1} : <span style="font-size: 1em;"><i class="fas fa-tv"></i></span></a><br>\n'.format(pfam_url, uni_id))
            url = "https://pfam.xfam.org/protein/{}?output=xml".format(uni_id)
            response = requests.get(url)
            if response.ok:
                rep = response.text
                id_list = re.findall("<match accession=\"(.*)\" id=\"(.*)\" type", rep) # Get the accesion name and the ID
                url_family = "https://pfam.xfam.org/family/"
                for id in id_list:
                    output_file.write("<a href=\"{0}{2}\">{1} : {2}</a><br>\n".format(url_family, id[0], id[1]))
            else:
                output_file.write("No Data Available")
        output_file.write("</div></td>\n")
    else:
        output_file.write("<td><div class=\"collapse\"> No Data Available </div></td\n>")
