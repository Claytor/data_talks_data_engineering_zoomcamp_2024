## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 
```bash 
docker --help
```

Now run the command to get help on the "docker build" command:
```bash
docker build --help
```

Do the same for "docker run".

```bash
docker run --help
```

Which tag has the following text? - *Automatically remove the container when it exits* 

```bash
--rm
```

```bash
docker run --rm [other-options] [image-name]
```

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.

```bash
docker run -it --entrypoint bash python:3.9`
```
Now check the python modules that are installed ( use ```pip list``` ). 
What is version of the package *wheel* ?

```bash
Package    Version
---------- -------
pip        23.0.1
setuptools 58.1.0
wheel      0.42.0
```

## Question 3. Count records 

We'll use the green taxi trips from September 2019:
Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)
 - How many taxi trips were totally made on September 18th 2019?
    > Tip: started and finished on 2019-09-18.
   
    > Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.
```sql
SELECT
	COUNT(lpep_pickup_datetime) AS pickup
FROM green_taxi_trips
	WHERE lpep_pickup_datetime >= '2019-09-18 00:00:00'
		AND lpep_pickup_datetime < '2019-09-19 00:00:00'
ORDER BY pickup DESC;
```

- 15767

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.
```sql
SELECT 
	CAST(lpep_pickup_datetime AS DATE) AS Day,
	MAX(trip_distance) AS Distance
FROM green_taxi_trips
GROUP BY CAST(lpep_pickup_datetime AS DATE)
ORDER BY Distance DESC
LIMIT 1;
```
- 2019-09-26

## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?

```SQL
SELECT 
    z."Borough",
    SUM(gt.total_amount) AS TotalRevenue
FROM green_taxi_trips AS gt
JOIN zones AS z
    ON gt."PULocationID" = z."LocationID"
WHERE CAST(gt.lpep_pickup_datetime AS DATE) = '2019-09-18'
    AND z."Borough" != 'Unknown'
GROUP BY z."Borough"
HAVING SUM(gt.total_amount) > 50000
ORDER BY TotalRevenue DESC
LIMIT 3;
```
- "Brooklyn" "Manhattan" "Queens"



## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

```sql
SELECT 
    dropoff_zone."Zone" AS DropoffZone,
    MAX(gt.tip_amount) AS LargestTip
FROM green_taxi_trips AS gt
JOIN zones AS pickup_zone
    ON gt."PULocationID" = pickup_zone."LocationID"
JOIN zones AS dropoff_zone
    ON gt."DOLocationID" = dropoff_zone."LocationID"
WHERE pickup_zone."Zone" = 'Astoria'
    AND DATE_TRUNC('month', gt.lpep_pickup_datetime) = DATE '2019-09-01'
GROUP BY dropoff_zone."Zone"
ORDER BY LargestTip DESC
LIMIT 1;
```

- JFK Airport

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.tcb-demo-bucket will be created
  + resource "google_bigquery_dataset" "tcb-demo-bucket" {
      + creation_time              = (known after apply)
      + dataset_id                 = "tcb_demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "zoomcamp-2024"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "tcb-terraform-demo-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value:
```
Paste the output of this command into the homework submission form.


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2024/homework/hw01
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: 29 January, 23:00 CET
