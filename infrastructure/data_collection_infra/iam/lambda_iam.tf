


resource "aws_iam_role" "lambda_execution_role" {
  name = var.lambda_execution_role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Lambda execution role for extract"
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Pricipal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

}

resource "aws_iam_role_policy" "lambda_execution_role_policy" {
  name = "${var.lambda_execution_role}-policy"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "LambdaAccessToS3"
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject"
        ]
        Resource = [
          "${aws_s3_bucket.jikan_data_lake.arn}/*",
          "${aws_s3_bucket.jikan_data_lake.arn}"
        ]
      },
      {
        Sid    = "LambdaLogGroupAccess"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      },
      {
        Sid    = "AllowLambdaToUseKMSKey"
        Effect = "Allow"
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "${aws_kms_key.anime_kms_key.arn}"
      }
    ]
  })
}

output "lambda_execution_role_arn" {
  value = aws_iam_role.lambda_execution_role.arn
}