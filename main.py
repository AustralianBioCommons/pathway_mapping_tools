
from scripts.functions import *

########################################################################################
### visit https://edamontology.github.io/edam-browser/ to navigate the EDAM ontology ###
########################################################################################

##############################
### operation URI examples ###
##############################

### operation_3926: pathway visualisation
### operation_3928: pathway analysis

operation_list = {"operation_3926": "pathway visualisation",
                  "operation_3928": "pathway analysis",
                  "operation_0276": "Protein interaction network analysis",
                  "operation_3929": "Metabolic pathway prediction"}

topic_list = {"topic_0602": "Molecular interactions, pathways and networks"}

### see https://pandas.pydata.org/docs/user_guide/merging.html#concatenating-objects
operation_dataframes = [ get_biotools_results_for_search_term(term = operation, search_type = "operationID") for operation in operation_list ]
topic_dataframes = [ get_biotools_results_for_search_term(term = topic, search_type = "topicID") for topic in topic_list ]

operation_result = pd.concat(operation_dataframes)
topic_result = pd.concat(topic_dataframes)

result = pd.concat([operation_result, topic_result])

result.to_csv("./returned_biotools_table.csv")
