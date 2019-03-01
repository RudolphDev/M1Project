import requests
import re


def Graph_prosite(string_uni, output_file):
    '''
    :param string_uni: uniprot_list joined
    :param output_file:
    :write: the viewer icon in the outputfile
    '''
    url_scan = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}".format(string_uni)
    response = requests.get(url_scan)
    if response.ok:
        html_page = response.text
        graph_link = re.findall("<a href=\"(.*)\">Graphical view</a>",html_page)
        output_file.write('<a href="{}"><span style="font-size: 1em;"><i class="fas fa-tv"></i></span></a><br>\n'.format(graph_link[0]))


def Prosite_parse(uniprot_list, output_file):
    '''
    :param uniprot_list:
    :param output_file:
    :write the PFAM domains and the viewer for each uniprot ID
    '''
    print("Querying Prosite...")
    if len(uniprot_list) != 0:  # Check if the uniprot list is not empty
        string_uni = "%0A".join(uniprot_list)  # Create a string with all the Uniprot ID
        url_rest = "https://prosite.expasy.org/cgi-bin/prosite/PSScan.cgi?seq={}&output=json".format(string_uni)
        response = requests.get(url_rest)
        if response.ok:
            json_result = response.json()
            i = 0
            output_file.write("<td><div class=\"collapse\">")
            Graph_prosite(string_uni, output_file) # Write the Graph icon to the viewer
            prosite_url = "https://prosite.expasy.org/"
            while i < len(json_result["matchset"]):  # Get all the domain for each uniprot ID
                prosite_acc = json_result["matchset"][i]["signature_ac"]  # Get the accession name for each domain
                prosite_id = json_result["matchset"][i]["signature_id"]  # Get the ID for each domain
                output_file.write('<a href=\"{0}{2}\">{1} : {2}</a><br>\n'.format(prosite_url, prosite_id, prosite_acc))
                i = i + 1
            output_file.write("</div></td>\n")
        else:
            output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')
    else:
        output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')

