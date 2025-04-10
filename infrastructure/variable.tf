

variable "aws_state_tracker" {
  description = "this is the name of the s3 bucket which will keep track of all the.tfstate files from the infrastructure in the CICD pipeline"
  type        = string
  sensitive = true
}
