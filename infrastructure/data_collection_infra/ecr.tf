resource "aws_ecr_repository" "lambda_repo" {
   name = var.ecr_repository
}
