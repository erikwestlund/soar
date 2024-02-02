#!/usr/bin/env bash

## Development tools and system dependencies
Rscript -e "install.packages('devtools', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('gitcreds', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('openssl', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('remotes', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('renv', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('rJava', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('rlang', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('rstudioapi', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('usethis', repos='https://cran.rstudio.com/')"

## Data management and wrangling packages
# Tidyverse includes: ggplot2, dplyr, tidyr, readr, purrr, tibble, stringr, forcats
Rscript -e "install.packages('tidyverse', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('broom', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('data.table', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('knitr', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('lubridate', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('purrr', repos='https://cran.rstudio.com/')"


# Database connection packages and utilities
Rscript -e "install.packages('DBI', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RJDBC', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RODBC', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RPostgres', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RSQLite', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('dbplyr', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('odbc', repos='https://cran.rstudio.com/')"

# Presentation utilities
Rscript -e "install.packages('table1', repos='https://cran.rstudio.com/')"
