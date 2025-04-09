
terraform {
  backend "s3" {
    bucket  = "s3-anime-analytics-infra-state-tracker"
    key     = "infra/terraform.tfstate"
    region  = "eu-central-1"
    encrypt = true
  }
  required_version = ">= 1.9.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.85.0"
    }
  }
}
provider "aws" {
  region = "eu-central-1"
}
