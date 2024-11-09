# Use a base image with R installed
FROM rocker/r-ver:4.3.0

# Install necessary system packages
RUN apt-get update && apt-get install -y curl build-essential python3 python3-pip

# Install dxpy using pip
RUN pip3 install dxpy

# Install additional R packages
RUN R -e "install.packages('glue', repos='https://cran.r-project.org')"

# Copy your Files into the container
COPY script.R /script.R
COPY field_list.txt /field_list.txt
COPY field_list_long.txt /field_list_long.txt
COPY run_script.sh /run_script.sh

# Set PATH environment variable for dx command
ENV PATH="$PATH:/root/.local/bin"

# Ensure the script is executable
RUN chmod +x /run_script.sh

# Set the entry point to run your Bash script
ENTRYPOINT ["/run_script.sh"]

