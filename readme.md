# UK Biobank Phenotype Data Extractor

This repository is a step-by-step guide for anyone, regardless of computer, Linux, or platform experience, to easily extract phenotype data from the UK Biobank. This guide covers using Docker and R with Glue, offering a clear alternative to using the Table Extract GUI. 

## Overview
There are two main ways to pull phenotype data from the UK Biobank:

1. **Table Extract (GUI method)** - This method can be challenging, even though it is meant to be straightforward.
2. **Docker & R with Glue** - This is the method detailed in this repository.

To get started, you'll need to create a `field_list.txt` file to specify the columns (fields) you need. Eventually, there will be another repository to help you create this file, along with one to batch pull the entire phenotype dataset.

The UK Biobank field format follows this structure:

```
p.[31m<FIELD-ID>[0m_i[34m<INSTANCE-ID>[0m_a[32m<ARRAY-ID>[0m
```

- **FIELD-ID**: [31mA unique ID for a feature (e.g., ALT liver blood marker).[0m
- **INSTANCE-ID**: [34mA number between 0-3 indicating the participant's visit (1st-4th).[0m
- **ARRAY-ID**: [32mA number (0-X) indicating the specific draw.[0m

Example: `[31mp4080[0m_[34mi0[0m_[32ma2[0m` means field ID [31m4080[0m, the first visit ([34mi0[0m), and the third draw ([32ma2[0m).

More information can be found [here](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=data_field).

## Prerequisites
1. **Access to UK Biobank Nexus**: [UK Biobank DNAnexus](https://ukbiobank.dnanexus.com/).
2. **UK Biobank Project**: An accepted project linked to your Nexus account.
3. **Level I UK Biobank Access** or above.
4. **Git Installation**: Install Git on Windows, Linux, or Mac.
    - **Windows**: Download the Git installer from [Git for Windows](https://gitforwindows.org/). Run the installer and follow the on-screen instructions, ensuring you select "Git Bash Here" during the installation process. Once installed, you can open Git Bash from the Start menu.
    - **Mac**: Run `brew install git` in Terminal.
    - **Linux**: Run `sudo apt install git` in Terminal.
5. **Docker Desktop**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/).
   - Docker Desktop must be running when you run the code.
6. **Dockerhub Username**: [Create an account here](https://hub.docker.com/signup).
7. **Create Docker Image on Dockerhub**: You will need this to store and share your Docker image.

## Step-by-Step Instructions

### Step 1: Install Docker Desktop and Create Dockerhub Username
- Download and install Docker Desktop: [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Create a Dockerhub username: [Sign up here](https://hub.docker.com/signup).

### Step 2: Clone the Repository
Open Terminal or Bash and run:
```
git clone https://github.com/UKBSidekick/ukb-extract.git
```
This will pull the repository onto your local machine. The resulting file structure should look like:

```
Root
- Dockerfile
- field_list.txt  # This file contains your selected fields
- field_list_long.txt  # Contains all available fields in UK Biobank; feel free to filter and use as needed
- readme.md  # This README file
- run_script.sh  # Script to be edited later
- script.R  # Script to be edited later
```
**Note**: Do not change any of the file names as it will break the process.

### Step 3: Edit `script.R`
Open `script.R` in RStudio or a text editor (Notepad, VSCode, etc.). You will need to modify the following lines:

```r
library(glue)

# Define your project_id, record or dataset_id & field_list file name

dataset_id = "project_id:record_id" 
field_list = paste(readLines("/field_list.txt"), collapse = ",")

# Shell command to extract dataset
template = "dx extract_dataset {dataset_id} --fields \"{field_list}\" -o filtered_data.csv"

cmd = glue::glue(template)
system(cmd)

# Example:
# dataset_id = "project-XXX:record-XXX" 
```

To get the **project_id**:
1. Log in to [DNAnexus Biobank](https://ukbiobank.dnanexus.com/).
2. Highlight your project (do not click).
3. Copy the project ID from the right window.

To get the **record_id**:
1. Click on your project to see files and folders.
2. Highlight `appXXX_XXXXX Dataset Record` and copy the `record-XXXXX` ID.

Save the modified `script.R` file.

### Step 4: Edit `run_script.sh`
Open `run_script.sh` with a plain text editor (e.g., Notepad on Windows):

```sh
#!/bin/bash

# Set DX authentication token (replace "your_token_here" with your actual token)
export DX_SECURITY_CONTEXT='{"auth_token_type": "Bearer", "auth_token": "your_token_here"}'

# Run the R script
Rscript /script.R
```

**Generate your API token**:
1. Log into [DNAnexus Biobank](https://ukbiobank.dnanexus.com/).
2. Click your profile picture > **My Profile** > **API TOKENS** tab.
3. Click **New Token**.
4. Name it, select "All projects", set an expiry date, and enter your password.
5. **Generate Token** and copy it (you cannot retrieve it again).

Replace `your_token_here` with the token you generated. Save the file as UTF-8 encoded, and ensure the extension is `.sh`.

### Step 5: Build Docker Image
Ensure Docker Desktop is running and you're logged in. In the terminal, navigate to the repository location and run:

```sh
docker build -t {dockerhub_username}/ukb-extract:latest .
```
Example:
```sh
docker build -t chonkie/ukb-extract:latest .
```

Push your Docker image to Dockerhub:
```sh
docker push {dockerhub_username}/ukb-extract:latest
```
Example:
```sh
docker push chonkie/ukb-extract:latest
```

### Step 6: Run Swiss Army Knife to Extract Data
1. Log in to [DNAnexus Biobank](https://ukbiobank.dnanexus.com/).
2. Click **Tools** > **Tools Library** > Find **Swiss Army Knife**.
3. Click **Run**.
4. Set the job name and output location.
5. Ignore input files.
6. In **Command Line**, type: `run_script.sh`.
7. In **Public Docker Image Identifier**, type: `{dockerhub_username}/ukb-extract:latest` (e.g., `chonkie/ukb-extract:latest`).
8. Click **Start Analysis** and **Launch Analysis**.

Monitor the job status under the **Monitor** tab. Once complete, your CSV will be available at the output location you specified.

## Conclusion
Congratulations on completing the setup! If you have any trouble, feel free to reach out. Please share if you find this helpful!

**Designed by chonkie**
