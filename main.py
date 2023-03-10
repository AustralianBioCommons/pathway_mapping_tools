
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
                  "operation_3928": "pathway analysis"}

### see https://pandas.pydata.org/docs/user_guide/merging.html#concatenating-objects
dataframes = [ get_biotools_results_for_search_term(term = operation, search_type = "operationID") for operation in operation_list ]
result = pd.concat(dataframes)

result.to_csv("./returned_biotools_table.csv")
