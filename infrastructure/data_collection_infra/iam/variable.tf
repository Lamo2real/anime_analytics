
variable "function_arn" {
  description = "arn of the Lambda function"
  type        = string
  sensitive   = true
}

variable "kms_arn" {
  description = "arn of the KMS key"
  type        = string
  sensitive   = true
}

variable "s3_bucket_arn" {
  description = "arn of the S3 bucket"
  type        = string
  sensitive = true
}

variable "lambda_execution_role" {
  default     = "jikan-extract-lambda-execution-role"
  description = "this is the lambda execution role base name"
  type        = string
}

variable "sfn_role_name" {
  default     = "anime-analytics-workflow-logic"
  description = "this is the name of the anime step functionns data flow stream"
  type        = string
}

variable "ecr_arn" {
  description = "this is the arn of ecr passed down from the parent directory"
  type = string
}