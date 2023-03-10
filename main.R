library(rmarkdown)
library(DT)
library(tidyverse)

# index page
rmarkdown::render("report.Rmd", output_file = "./docs/index.html")
