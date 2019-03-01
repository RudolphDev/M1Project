import requests
import re


def Gene_parse(gene_symbol, organism, output_file):
    """
    :param gene_symbol:
    :param organism:
    :param output_file:
    Write the gene id and name in the file
    :return: the list of gene id
    """
    print("Querying Gene...")
    url = """https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term={}[ORGN] {}[sym]
            &retmode=json""".format(organism, gene_symbol)
    response = requests.get(url)
    if response.ok:
        json_rep = response.json()
        list_id = json_rep["esearchresult"]["idlist"]
        output_file.write("<td><div class=\"collapse\">")
        for id in list_id:
            url_efetch = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id={}&retmode=xml".format(id)
            response = requests.get(url_efetch)
            if response.ok:
                re_text = response.text
                name_list = re.findall('<NomenclatureName>(.*)</NomenclatureName>', re_text)  # Get the Name from XML file
                if name_list != [""]:  # Check if the Gene List is not empty
                    full_name = name_list[0]  # Get the first elem as full name
                else:
                    full_name= "No Name Available"
            else:
                full_name = "No Name Available"
            clean_full_name = re.sub("([,/].*)", "", full_name) # Clean the name to remove parenthesis
            output_file.write('<a href="https://www.ncbi.nlm.nih.gov/gene/{0}">{0} : {1}</a><br>\n'.format(id, clean_full_name))
        output_file.write("</div></td>\n")
    else:
        output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
    return(list_id)


def Refseq_parse(db, type, organism, gene_symbol, output_file):
    """
    :param db: Name of the RefSeq database (Nucleotide or Protein)
    :param type: of the id M for the mRNA and P for protein
    :param organism:
    :param gene_symbol:
    :param output_file:
    :write the ID in the file and a link to UCSC for NM
    """
    print("Querying RefSeq {}...".format(db))
    url = """https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db={}&term=({}[ORGN]+{}[Gene%20Name])
            &idtype=acc&retmode=json""".format(db, organism, gene_symbol)
    response = requests.get(url)
    if response.ok:
        json_rep = response.json()
        list_id = json_rep["esearchresult"]["idlist"]  # Get the ID from the JSON file
        clean_list = []
        for id in list_id:
            if "{}_".format(type) in id:  # Keep only the ID with the right format (NM_ XM)
                clean_list.append(id)
        if len(clean_list) != 0:
            output_file.write('<td><div class=\"collapse\">')
            for id in clean_list:
                if "NM" in id:  # Check if the function is for nucleotide then add the UCSC link
                    ucsc_url = "http://genome.ucsc.edu/cgi-bin/hgTracks?org={}&position={}".format(organism, id)
                    output_file.write("""<a href="{1}{0}"><span style="font-size: 1em;"><i class="fas fa-tv"></i></span></a>\n
                                <a href="https://www.ncbi.nlm.nih.gov/nuccore/{0}">{0}</a><br>\n
                            """.format(id, ucsc_url))
                else:
                    output_file.write('<a href="https://www.ncbi.nlm.nih.gov/nuccore/{0}">{0}</a><br>\n'.format(id))
            output_file.write('</div></td>\n')
        else:
            output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
    else:
        output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")

