library(glue)

# Define your project_id, record or dataset_id & field_list file name
dataset_id = "project_id:record_id"
field_list = paste(readLines("/field_list.txt"), collapse = ",")

# R code with shell command
template = "dx extract_dataset {dataset_id} --fields \"{field_list}\" -o filtered_data.csv"

cmd = glue::glue(template)
system(cmd)

# Note
# project_id would be: project-XXX
# record_id or data would be: record-XXX

# The edited line would look like the following
# dataset_id = "project-XXX:record-XXX" 