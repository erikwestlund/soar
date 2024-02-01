#!/usr/bin/env bash

Rscript -e "install.packages('devtools', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('remotes', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('tidyverse', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('renv', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('DBI', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('rJava', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RPostgres', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RSQLite', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('odbc', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RODBC', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('RJDBC', repos='https://cran.rstudio.com/')"
