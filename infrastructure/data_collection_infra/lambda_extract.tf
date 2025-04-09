locals {
  path = "${path.module}/../../application/"
}

module "iam" {
  source = "./iam/"
}

resource "aws_lambda_function" "extract_anime_data" {
  filename      = "${local.path}extract_load_script.zip"
  function_name = var.lambda_infra_name
  handler       = "${var.lambda_file_name}.${var.lambda_file_function_name}"
  role          = module.iam.lambda_execution_role_arn
  runtime       = "python3.13"
  timeout       = 60
  memory_size   = 256
  architectures = ["x86_64"]

  kms_key_arn = aws_kms_key.anime_kms_key.arn

  source_code_hash = filebase64sha256("${local.path}extract_load_script.zip")

}

output "lambda_arn" {
  value = aws_lambda_function.extract_anime_data.arn
}