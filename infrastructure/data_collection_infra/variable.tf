

variable "anime_etl_region" {
  default     = "eu-central-1"
  description = "this is merely a value for where the infrastructure is in the cloud of aws"
  type        = string
}

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
variable "lambda_infra_name" {
  default     = "anime-lambda-function-name"
  description = "this is the name of the lambda infra configuration name"
  type        = string
}

variable "s3_data_lake_name" {
  default     = "anime-s3-data-lake-name"
  description = "this is the name of the s3 data lake that holds the data extracted from jikan API"
  type        = string
}

