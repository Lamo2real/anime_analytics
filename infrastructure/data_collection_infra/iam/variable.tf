

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
