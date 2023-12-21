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

**Next steps are:**

- Make postgres run in docker
- Import NY taxi data
- GCP infrastructure with Terraform.

Notes:
- Build container: `docker build -t test:pandas .`
- Run docker `docker run -it test:pandas`