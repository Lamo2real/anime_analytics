
locals {
  path = "${path.module}/../../application"
}

module "iam" {
  source           = "./iam"
   
  sfn_arn          = aws_sfn_state_machine.wrokflow.arn
  s3_bucket_arn    = aws_s3_bucket.jikan_data_lake.arn  
  kms_arn          = aws_kms_key.anime_kms_key.arn
  function_arn     = aws_lambda_function.extract_anime_data.arn
  ecr_arn          = aws_ecr_repository.lambda_repo.arn
}

resource "aws_lambda_function" "extract_anime_data" {
  function_name = var.lambda_infra_name
  
  package_type  = "Image"
  image_uri     = var.docker_image_uri
  role          = module.iam.lambda_execution_role_arn
  timeout       = 120
  memory_size   = 512
  architectures = ["x86_64"]

  environment {
    variables = {
      BUCKET_NAME = var.s3_data_lake_name
      S3_KEY_PATH = var.s3_path_to_processed_data_file
    }
  }
}
