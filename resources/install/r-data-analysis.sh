#!/usr/bin/env bash

# Make sure devtools is installed
Rscript -e "install.packages('devtools', repos='https://cran.rstudio.com/')"

# Data analysis packages
Rscript -e "install.packages('cmdstanr', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('lme4', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('lmerTest', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('mice', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('rstan', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('rstanarm', repos='https://cran.rstudio.com/')"

# McElreath's Rethinking Universe
Rscript -e "install.packages('coda', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('mvtnorm', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('loo', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('dagitty', repos='https://cran.rstudio.com/')"
Rscript -e "install.packages('shape', repos='https://cran.rstudio.com/')"
Rscript -e "devtools::install_github('rmcelreath/rethinking')"

# Biomedical analysis utilities
Rscript -e "install.packages('comorbidity', repos='https://cran.rstudio.com/')"

