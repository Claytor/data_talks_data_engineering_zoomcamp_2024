variable "credentials" {
  description = "My Credentials"
  default     = "../credentials/zoomcamp-2024-8326022942ed.json"
  #ex: if you have a directory where this file is called keys with your service account json file
}

variable "project" {
  description = "Claytor DE Bootcamp"
  default = "zoomcamp-2024"
}

variable "region" {
  description = "Region"
  #Update the below to your desired region
  default     = "us-south1"
}

variable "location" {
  description = "Project Location"
  #Update the below to your desired location
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "tcb_demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  #Update the below to a unique bucket name
  default     = "tcb-terraform-demo-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}