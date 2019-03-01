import requests


def go_parse(uniprot_list, go_type, output_file):
    '''
    :param uniprot_list:
    :param go_type:
    :param output_file:
    :write: the Go names for the list of Uniprot ID.
    '''
    print("Querying Go term " + go_type + "...")
    if len(uniprot_list) != 0:  # CHeck if the Uniprot list is not empty
        uniprot_string = ','.join(uniprot_list)  # Join all the uniprot ID for the query
        url_id = "https://www.ebi.ac.uk/QuickGO/services/annotation/search?includeFields=goName&aspect=" + go_type + "&geneProductId=" + uniprot_string
        r_id = requests.get(url_id, headers={"Accept": "application/json"})  # Request with a JSON output

        if r_id.ok:  # Check if the result works
            response = r_id.json()
            list_go = []
            output_file.write("<td><div class=\"collapse\">")
            url = "https://www.ebi.ac.uk/QuickGO/term/"
            i = 0
            while i < len(response['results']):  # Parse the JSON file for each go ID
                if response['results'][i]['goId'] not in list_go:  # Check if the goID is already written or not
                    list_go.append(response['results'][i]['goId'])
                    go_id = response['results'][i]['goId']
                    go_name = response['results'][i]['goName']
                    output_file.write('<a href="{}{}">{}</a><br>\n'.format(url, go_id, go_name))
                i = i + 1
            output_file.write("</div></td>\n")
        else:
            output_file.write('<td><div class=\"collapse\"> QuickGO not Available </div></td>\n')

    else:
        output_file.write('<td><div class=\"collapse\"> No Data Available </div></td>\n')


