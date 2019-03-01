import requests


def ensembl_request(db_name, gene_symbol, organism):
    """
    :param db_name:
    :param gene_symbol:
    :param organism:
    :return: the result from the query
    """
    server = "https://rest.{}.org".format(db_name)  # get the ensembl name url
    ext = "/xrefs/symbol/{}/{}?".format(organism, gene_symbol) # Create the URL with the organism and the gene symbol
    response = requests.get(server + ext, headers={"Content-Type": "application/json"})
    return response


def ensembl_test_urls(organism, base, letter, id, output_file):
    """
    :param organism:
    :param base: from the url Gene Transcript or Protein
    :param letter: indicate the letter of the id type
    :param id:
    :param output_file:
    :return: Test the different URL from the different ensembl databases and write the result in the html file.
    """
    db_list = ["ensembl", "plants.ensembl", "bacteria.ensembl", "fungi.ensembl", "protists.ensembl", "metazoa.ensembl"]
    for db in db_list:
        final_url = "http://{}.org/{}/{}Summary?db=core;{}={}".format(db, organism, base, letter, id)
        test_url = requests.get(final_url)
        if test_url.ok: # test if the URL is good, if good write the html else, check another database name
            if letter == "g": # For the Gene Column, add the icon to the genome browser and the ortholog list
                gb_url = "http://www.{}.org/{}/Location/View?db=core;g={}".format(db, organism, id)
                lo_url = "http://www.{}.org/{}/Gene/Compara_Ortholog?db=core;g={}".format(db, organism, id)
                output_file.write("""<a href="{2}"><span style="font-size: 1em;"><i class="fas fa-tv"></i></span></a>\n
                            <a href="{3}"><span style="font-size: 1em;"><i class="fas fa-list-ul"></i></span></a>\n
                            <a href="{0}">{1}</a><br>\n
                            """.format(final_url, id, gb_url, lo_url))
            else:
                output_file.write('<a href="{}">{}</a><br>\n'.format(final_url, id))
            break # if the url is ok stop the for loop


def ensembl_write(response, organism, output_file):
    """
    :param response: get JSON from URL request
    :param organism:
    :param output_file:
    :return:
    """
    decoded = response.json()
    i = 0
    list_gene = []
    output_file.write('<td><div class="collapse">')
    if len(decoded) != 0: # Check if the JSON is not empty
        while i < len(decoded): # Parse all the occurencies in the JSON
            list_gene.append(decoded[i]['id']) # Add the Gene ID to a list
            ensembl_test_urls(organism, "Gene/", "g", decoded[i]['id'], output_file) # Test the different url and write the result
            i = i + 1
        output_file.write('</div></td>\n')
    else:
        output_file.write(" No Data Available </div></td>\n")
    return list_gene


def ensembl_information_request(db_name, string_ids):
    """
    :param db_name:
    :param string_ids:
    :return: the response from the query
    """
    server = "https://rest.{}.org".format(db_name)
    ext = "/lookup/id/"
    headers = {"Content-Type": "application/json;expand=1"}
    response = requests.post(server + ext, headers=headers, data='{ "ids" : [' + string_ids + '], "expand" : 1 }')
    return response


def ensembl_information(list_gene, db_name, organism, output_file):
    """
    Get the information from the list of gene ID
    :param list_gene:
    :param db_name:
    :param organism:
    :param output_file:
    :return: Call the function to write the Transcript and Protein data
    """
    list_gene_quote = ['"{0}"'.format(element) for element in list_gene]  # Delete the quotes from the list of ID
    string_ids = ",".join(list_gene_quote)  # Join all the elem in a String
    response = ensembl_information_request(db_name, string_ids) # Get the JSON from the function
    if response.ok:  # Check if the result URL is good
        decoded = response.json() # get the JSON form the URL response
        output_file.write('<td><div class="collapse">')
        for gene_id in list_gene:  # The JSON is divided by gene ID
            if decoded[gene_id] != None: # Check if the JSON is not empty
                i = 0
                while i < len(decoded[gene_id]['Transcript']): # Parse The JSON for each occurrences
                    # Use the function to Write all the Transcript in the HTML file
                    ensembl_test_urls(organism, "Transcript/", "t", decoded[gene_id]['Transcript'][i]['id'], output_file)
                    i = i + 1
        output_file.write('</div></td>\n')
        output_file.write('<td><div class="collapse">')
        for gene_id in list_gene: # Do the same as before but more specific for the Protein
            if decoded[gene_id] != None:
                i = 0
                while i < len(decoded[gene_id]['Transcript']):
                    if decoded[gene_id]['Transcript'][i]['biotype'] == "protein_coding": # Check if the transcript is a Protein coding
                        ensembl_test_urls(organism, "Transcript/Protein", "p", decoded[gene_id]["Transcript"][i]['Translation']['id'], output_file)
                    i = i + 1

        output_file.write('</div></td>\n')
    else:
        output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
        output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")


def ensembl_parse(gene_symbol, organism, output_file):
    """
    :param gene_symbol:
    :param organism:
    :param output_file:
    :return: Call functions to write all the information from EnsEMBL
    """
    print("Querying EnsEMBL...")
    response = ensembl_request("ensembl", gene_symbol, organism) # Do a first request with ensembl
    if response.ok:
        list_gene = ensembl_write(response, organism, output_file) # write the Gene ID and get it to fetch information
        if len(list_gene) != 0: # Check if the gene list is not empty
            ensembl_information(list_gene, "ensembl", organism, output_file) # Use the function to write all the information
        else:
            output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
    else:  # If ensembl doesn't work try with ensemblgenomes
        response = ensembl_request("ensemblgenomes", gene_symbol, organism) # DO the same as before but with ensemblgenome
        if response.ok:
            list_gene = ensembl_write(response, organism, output_file)
            if len(list_gene) != 0:
                ensembl_information(list_gene, "ensemblgenomes", organism, output_file)
            else:
                output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
                output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
        else:
            output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
            output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
            output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
