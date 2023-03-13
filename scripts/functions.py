
import math
import pandas as pd
import requests
import json

#########################
### code adapted from ###
#########################

### https://github.com/AustralianBioCommons/australianbiocommons.github.io/blob/84b42b19370ab8133453c4757ba5edffc62ce360/finders/toolfinder.py
### see license here: https://github.com/AustralianBioCommons/australianbiocommons.github.io/blob/c759d99a32f4d345e3601c7113a1951cd54d825e/LICENSE

##########################
### search_id examples ###
##########################

### operationID - this is used as follows https://bio.tools/api/t/?format=json&operationID="[operation URI]"
### topicID - this is used as follows https://bio.tools/api/t/?format=json&topicID="[topic URI]"


def get_biotools_results_for_search_term(term, search_type):

    biotools_url = "https://bio.tools/api/t/?format=json&%s=\"%s\"" % (search_type, term)

    # see https://bio.tools/api/t/?operationID=%22operation_3083%22
    response = requests.get(biotools_url)
    tool_metadata = json.loads(response.text)

    # see https://stackoverflow.com/a/24049334
    # https://bio.tools/api/t/?format=json&operationID=%22operation_3083%22&page=2
    # see https://stackoverflow.com/a/71664742
    number_pages = math.ceil(tool_metadata["count"]/10)

    url_array = []
    for page in range(1, number_pages):
        url = """%s"&page=%s""" % (biotools_url, page)
        url_array.append((page, url))

    available_data = {}
    # see https://stackoverflow.com/a/72861816
    for page, url in url_array:
        response = requests.get(url)
        if response.status_code != 200:
            raise FileNotFoundError(response.url)
        tool_metadata = json.loads(response.text)
        for tool in tool_metadata["list"]:
            tool_id = tool["name"]
            available_data[tool_id] = tool

    formatted_list = []
    for i in available_data:
        data = available_data[i]
        tool_line = []
        tool_line.append("<a href='https://bio.tools/%s'>%s</a>" % (data["biotoolsID"], data["name"]))
        tool_line.append(", ".join(x["term"] for x in data["function"][0]["operation"]))
        tool_line.append(", ".join(x["term"] for x in data["topic"]))
        if isinstance(data["publication"], list):
            tool_line.append(", ".join(list(map(lambda x:f"""<a href="https://doi.org/{x["doi"]}">{x["metadata"]["title"] if x["metadata"] is not None else "DOI:" + x["doi"]}</a>""" if x["doi"] is not None else
                                                f"""<a href="http://www.ncbi.nlm.nih.gov/pubmed/{x["pmid"]}" >{x["metadata"]["title"] if x["metadata"] is not None else "PMID:" + x["pmid"]}</a>""" if x["pmid"] is not None else
                                                f"""<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/{x["pmcid"]}" >{x["metadata"]["title"] if x["metadata"] is not None else "PMCID:" + x["pmcid"]}</a>""" if x["pmcid"] is not None else "",
                                                data["publication"]))))
        else:
            tool_line.append("")
        tool_line.append(", ".join(["""<p>%s</p>""" % x for x in data["language"]]))
        if isinstance(data["publication"], list):
            tool_line.append(", ".join(list(map(lambda x:f"""https://doi.org/{x["doi"]}""" if x["doi"] is not None else
                                                f"""http://www.ncbi.nlm.nih.gov/pubmed/{x["pmid"]}""" if x["pmid"] is not None else
                                                f"""https://www.ncbi.nlm.nih.gov/pmc/articles/{x["pmcid"]}""" if x["pmcid"] is not None else "",
                                                data["publication"]))))
        tool_line.append(term)
        tool_line.append(search_type)
        formatted_list.append(tool_line)

    table = pd.DataFrame(formatted_list, columns = ["name_biotools_link", "operation", "topic", "publication", "language", "publication_url", "search term ID", "search_type"])

    return(table)