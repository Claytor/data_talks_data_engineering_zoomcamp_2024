# Claytor's Log

## Module 1: Introduction & Prerequisites

### 12/20/2023

**Today I:**

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

- Pull docker image: `docker pull postgres:13`
- Build container: `docker build -t test:pandas .`
- Run docker `docker run -it test:pandas`

### 12/21/2023

- Worked on ingesting data into docker file
- Struggled with port configuration.  I'll handle it tomorrow

### 12/22/2023

- Was able to successfully create postgres container.
- Explored container with pgcli
- Used sqlalchemy inside of a jupyter notebook to successfuly ingest data to postgres container.  Verified results with pgcli

**Next steps are:**
- create a pgadmin container and network with postgres container