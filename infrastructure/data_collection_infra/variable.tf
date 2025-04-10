
# configured in CI/CD pipeline
####################################################################################
variable "anime_etl_region" {
  description = "this is merely a value for where the infrastructure is in the cloud of aws"
  type        = string
  sensitive = true
}

variable "lambda_infra_name" {
  description = "this is the name of the lambda infra configuration name"
  type        = string
  sensitive = true
}

variable "s3_data_lake_name" {
  description = "this is the name of the s3 data lake that holds the data extracted from jikan API"
  type        = string
  sensitive = true
}

variable "s3_path_to_processed_data_file" {
  description = "this is the path to the file to the csv in s3"
  type        = string
  sensitive = true
}
####################################################################################





variable "lambda_file_name" {
  default     = "transform_anime_data"
  description = "this is the name of the python file which is run in lambda"
  type        = string
}
variable "lambda_file_function_name" {
  default     = "transform"
  description = "this is the name of the function in the python file which is run in lambda"
  type        = string
}


