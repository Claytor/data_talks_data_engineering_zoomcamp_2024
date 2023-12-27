# Claytor's Log

## Module 1: Introduction & Prerequisites

### 12/20/2023 - Setup

- Set-up GCP account through CLI and made a new project in Google cloud.
- Installed Docker and Docker Compose.
- Installed Terraform
- Prepared a working environment for the course
- Successfuly created a few trial containers.
  - Made Dockerfile
    - Runs python 3.1
    - Installs Pandas
    - ENTRYPOINT at 'python', 'pipeline.py'
  - Created pipeline (pipeline.py)
    - imports sys and pandas
- Successfully built and tested a container that takes an argument and gives an expected result! 😂
- Basic workflow notes
  - Pull docker image: `docker pull 'name_of_container'`
  - Build container: `docker build -t 'name_of_container' .`
  - Run docker `docker run -it 'name_of_container'`

### 12/21/2023 - Ingestion configuration

- Worked on ingesting data into docker file
- Struggled with port configuration.  Couldn't get my data to where it needed to be.  The issue was that my local installation of pgAdmin was already running on the default port.  I had to I'll handle it tomorrow

### 12/22/2023 - First attempt at Docker Network

- Was able to successfully create postgres container.
- Explored container with pgcli
- Used sqlalchemy inside of a jupyter notebook to successfuly ingest data to postgres container.  Verified results with pgcli

### 12/23/2023 - Lots of progress and hard lessons learned

- Created pgAdmin container and accessed it through localhost
- Attempted to setup docker network for both pgadmin and postgres. Kept running into issues
  - Found the source of the errors was from whitespace in code being run in terminal
  - ⚠️ **CHECK YOUR BASH COMMANDS IN EDITOR FOR WHITESPACE BEFORE PASTING INTO TERMINAL** 😤
- Accidentily deleted postgres container with injested data  🥴.  Didn't take too long to recreate, but it would have sucked if that happened with a larger database.  Not too much trouble to run the notebook again.  Since I'm using parquet files, It makes me kind of nervous not to be able to see the progress from within the notebook . . . I'll propably need a better monitoring strategy in the future.
  - ⚠️ **MAKE SURE YOU SHUT YOUR CONTAINERS DOWN PROPERLY OR SUFFER THE CONSEQUENCES!!!**
- I was able to get the containers networkd and talking together.  I'm so stoked I figured it out!
- Converted ipynb to python script using `jupyter nbconvert` to make a 'poboy' ingestion script.
  - Used argparse library to parse arguements to containers
  - This is referred to as a **top-level code environment**  and required a main block `if __name__ == '__main__':`.  I dont exactly know the broader context of why its needed here, but the instructor said it was needed for things we want to run as scripts.
- Dropped taxi data from container to test script
- I was running the script bind and it was erroring out.  Went down a rabbit hole for error handling.
- OMG IT WORKED!!!!!  I successfully ingested data to my containers with a python script!  It ain't much, but its mine!

#### **12/27/2023** - Making an ingestion container to apply ingestion script to docker network

- Fixed python script do download data to the intended local directory
- Continued to run into confusion about local network vs. docker network.  I got it ironed out.
- I was able to create a container that:
  - connected to docker network containing postgres and pgadmin container
  - installed dependencies to run python ingestion script
  - programatically downloaded local parque file and ingested data to networked postgress database.
  - confirmed success with pgAdmin container.

#### **Next steps are:**

- write docker compose file
