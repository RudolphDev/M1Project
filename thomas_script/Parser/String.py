import requests


def string_parse(uniprot_list, output_file):
    """
    :param uniprot_list:
    :param output_file:
    :write string URL in html file;
    """
    if len(uniprot_list) != 0:  # Check if an Uniprot ID exist
        url = "https://string-db.org/api/highres_image/network?identifiers="
        print("Querying String...")
        output_file.write("<td><div class=\"collapse\">")
        i = 0
        for uni_id in uniprot_list:  # For each Uniprot ID Create the URL
            full_url = url + uni_id
            response = requests.get(full_url)
            if response.ok:  # Check if the URL exist
                # Write the link in html file
                output_file.write('<a href="{0}{1}"><span style="font-size: 1em;"><i class="fas fa-code-branch"></i></span> {1} interaction map </a><br>'.format(url, uni_id))
                i = i + 1
        if i == 0:  # Check if no url was good then write no data
            output_file.write("No Data Available")
        output_file.write("</div></td>\n")
    else:
        output_file.write("<td><div class=\"collapse\"> No Data Available </div></td>\n")
