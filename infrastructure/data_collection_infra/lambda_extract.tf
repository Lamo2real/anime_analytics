
locals {
  path = "${path.module}/../../application"
}

module "iam" {
  source           = "./iam"
   
  s3_bucket_arn    = aws_s3_bucket.jikan_data_lake.arn  
  kms_arn          = aws_kms_key.anime_kms_key.arn
  function_arn     = aws_lambda_function.extract_anime_data.arn
}

resource "aws_lambda_function" "extract_anime_data" {
  filename      = "${local.path}/extract_load_script.zip"
  function_name = var.lambda_infra_name
  handler       = "${var.lambda_file_name}.${var.lambda_file_function_name}"
  role          = module.iam.lambda_execution_role_arn
  runtime       = "python3.13"
  timeout       = 60
  memory_size   = 256
  architectures = ["x86_64"]

  kms_key_arn = aws_kms_key.anime_kms_key.arn

  source_code_hash = filebase64sha256("${local.path}/extract_load_script.zip")

  environment {
    variables = {
      BUCKET_NAME = var.s3_data_lake_name
      S3_KEY_PATH = var.s3_path_to_processed_data_file
    }
  }
}
