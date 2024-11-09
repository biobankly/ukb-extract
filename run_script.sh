#!/bin/bash

# Set DX authentication token (replace "your_token_here" with your actual token)
export DX_SECURITY_CONTEXT='{"auth_token_type": "Bearer", "auth_token": "your_token_here"}'

# Run the R script
Rscript /script.R
