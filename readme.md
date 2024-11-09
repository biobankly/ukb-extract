![UK Biobank Logo](/images/uk_biobank.png)
# UK Biobank Phenotype Data Extractor

This repository is a step-by-step guide for anyone, regardless of computer, Linux, or platform experience, to easily extract phenotype data from the UK Biobank. This guide covers using Docker and R with Glue, offering a clear alternative to using the Table Extract GUI. 


## Overview
There are two main ways to pull phenotype data from the UK Biobank:

1. **Table Extract (GUI method)** - This method can be challenging, even though it is meant to be straightforward.
2. **Docker & R with Glue** - This is the method detailed in this repository.

> [!IMPORTANT]
> To get started, you'll need to create a `field_list.txt` file to specify the columns (fields) you need. Eventually, there will be another repository to help you create this file, along with one to batch pull the entire phenotype dataset.

> [!TIP]
> The UK Biobank field format follows this structure:

```
p.<FIELD-ID>_i<INSTANCE-ID>_a<ARRAY-ID>
```

- **FIELD-ID**: A unique ID for a feature (e.g., ALT liver blood marker).
- **INSTANCE-ID**: A number between 0-3 indicating the participant's visit (1st-4th).
- **ARRAY-ID**: A number (0-X) indicating the specific draw.

Example: `p4080_i0_a2` means field ID 4080, the first visit (i0), and the third draw (a2).

More information can be found [here](https://biobank.ndph.ox.ac.uk/ukb/help.cgi?cd=data_field).


> [!NOTE]
> ## Prerequisites 🚀
> 1. **Access to UK Biobank Nexus**: [UK Biobank DNAnexus](https://ukbiobank.dnanexus.com/).
> 2. **UK Biobank Project**: An accepted project linked to your Nexus account.
> 3. **Level I UK Biobank Access** or above.
> 4. **Git Installation**: Install Git on Windows, Linux, or Mac.
>     - **Windows**: Download the Git installer from [Git for Windows](https://gitforwindows.org/). Run the installer and follow the on-screen instructions, ensuring you select "Git Bash Here" during the installation process. Once installed, you can open Git Bash from the Start menu.
>     - **Mac**: Run `brew install git` in Terminal.
>     - **Linux**: Run `sudo apt install git` in Terminal.
> 5. **Docker Desktop**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop/).
>    - Docker Desktop must be running when you run the code.
> 6. **Dockerhub Username**: [Create an account here](https://hub.docker.com/signup).
> 7. **Create Docker Image on Dockerhub**: You will need this to store and share your Docker image.


## Step-by-Step Instructions 📋


### Step 1: Install Docker Desktop and Create Dockerhub Username
- Download and install Docker Desktop: [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Create a Dockerhub username: [Sign up here](https://hub.docker.com/signup).


### Step 2: Clone the Repository
Open Terminal on Windows or Bash on Mac or Linux:
- Navigate to a folder location where you would like to save this project
- Use commands cd etc and mkdir to get there
- When ready and in location run:
```
git clone https://github.com/UKBSidekick/ukb-extract.git
```
This will pull the repository onto your local machine. The resulting file structure should look like:

```
UKB-Extract/
└── Dockerfile
└── field_list.txt  # This file contains your selected fields
└── field_list_long.txt  # Contains all available fields in UK Biobank; feel free to filter and use as needed
└── readme.md  # This README file
└── run_script.sh  # Script to be edited later
└── script.R  # Script to be edited later
```
> [!CAUTION]
> **NOTE**: DO NOT CHANGE ANY OF THE FILE NAMES AS IT WILL BREAK THE PROCESS.


### Step 3: Edit `script.R` ✏️
Open `script.R` in RStudio or a text editor (Notepad, VSCode, etc.). You will need to modify the following lines:

```r
library(glue)

# Define your project_id and record_id with your own id's as explained below

dataset_id = "project_id:record_id" 
field_list = paste(readLines("/field_list.txt"), collapse = ",")

template = "dx extract_dataset {dataset_id} --fields \"{field_list}\" -o filtered_data.csv"

cmd = glue::glue(template)
system(cmd)

# Example:
# dataset_id = "project-XXX:record-XXX"
```

To get the **project_id**:
1. Log into the DNAnexus Biobank [https://ukbiobank.dnanexus.com/](https://ukbiobank.dnanexus.com/).
2. Highlight the project you want to work on, do not click it! It will open into another window. You just want to highlight it.
3. A window will open from the right with your project details.
4. Under Project ID, you can copy the ID and paste it into the script.

To get the **record_id**:
1. Log into the DNAnexus Biobank as above.
2. This time click on your project instead of highlighting it.
3. You will see some files and folders in the root directory.
4. You should be able to see two files:
   - `appXXX_XXXXX Dataset Record`
   - `appXXX_XXXXX Database`
5. Don't click but highlight the `appXXX_XXXXX Dataset Record` line.
6. A window will pop out from the right.
7. It should give you the details of the record and the ID.
8. Copy the ID which is called `record-XXXXX`.
9. Copy this in the `script.R` code.

You can now save the `script.R` code.


### Step 4: Edit `run_script.sh` ✏️
Open `run_script.sh` with a plain text editor (e.g., Notepad on Windows):

```sh
#!/bin/bash

# Set DX authentication token (replace "your_token_here" with your actual token)
export DX_SECURITY_CONTEXT='{"auth_token_type": "Bearer", "auth_token": "your_token_here"}'

# Run the R script
Rscript /script.R
```

You will need to get a key from the UK Biobank to replace the "your_key_here"

Steps to create a key:
1. Log into the DNAnexus Biobank [https://ukbiobank.dnanexus.com/](https://ukbiobank.dnanexus.com/).
2. Once logged in, click on the top right corner on your profile picture and select **My Profile**.
3. A new window will appear with four tabs at the top: **User Account**, **Billing**, **Account Security**, and **API TOKENS**.
4. Click on **API TOKENS**.
5. Click **New Token**.
6. Give the token a label (it can be anything, e.g., `ukb-extract`).
7. Select **All projects**.
8. Set an expiry date for security (choose a reasonable time frame until you still need the token).
9. Enter your DNAnexus password. Note: The box is tricky to see, but it's there. Click on it and enter your password.
10. **Generate Token**.

Once your token is generated, you can copy it. **REMEMBER**, once you close this window, you will not be able to retrieve your token again. If you forget or need to retrieve the token, you will not be able to and would need to create another token.

Replace the `your_token_here` part in the `run_script.sh` file:

```sh
export DX_SECURITY_CONTEXT='{"auth_token_type": "Bearer", "auth_token": "your_token_here"}'
```
Example:
```sh
export DX_SECURITY_CONTEXT='{"auth_token_type": "Bearer", "auth_token": "XXXXxxxXXXxxxXX"}'
```

> [!CAUTION]
> **Now save the file: and very important for Windows users!! Remember to save it as UTF-8, otherwise it won't work.**

Go to **File > Save As**.
- Select **All Files (*.*)** as the file type.
- Name the file with a `.sh` extension, e.g., `script.sh`.
- Ensure the encoding is set to **UTF-8** and save it to your desired location. **This is an incredibly important step. If you don't choose UTF-8, it will not work.** 


### Step 5: Build Docker Image 🐳
Ensure Docker Desktop is running and you're logged in. In the terminal on Windows and bash on Mac or Linux, navigate to the repository location, which is  and run:

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
Finally: 🔑
1. Log into the DNAnexus Biobank [https://ukbiobank.dnanexus.com/](https://ukbiobank.dnanexus.com/).
2. At the top, click on **Tools** and select **Tools Library**.
3. Scroll down to an app or tool called **Swiss Army Knife**.
4. Click on it and select **Run**.
5. Select your **Job Name**, which can be anything, and the output location of where you would like to place the CSV file. Click **Next**.
6. Ignore **Input files** and **Platform file**.
7. In the **Command Line**, type: `run_script.sh`.
8. In the **Public Docker Image Identifier**, type: `{dockerhub_username}/ukb-extract:latest` (e.g., `chonkie/ukb-extract:latest`).
9. Click the top right **Start Analysis**.
10. Choose your criteria and your compute specifications, just ignore if you are unsure.
11. Click **Launch Analysis**.

✅ Your job should now be viewable in the **Monitor** tab when you click **Projects**. Depending on your `field_list.txt` file size, it might take some time to create the file.

Once finished, it should show **Complete**, and your file should pop up at the output location you specified for **Swiss Army Knife**.



## Conclusion
Congratulations on completing the setup! If you have any trouble, feel free to reach out. Please share if you find this helpful!

**Designed by chonkie**