

resource "aws_iam_role" "lambda_execution_role" {
  name = var.lambda_execution_role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "LambdaExecutionRoleForExtract"
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
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
          "${var.s3_bucket_arn}/*",
          "${var.s3_bucket_arn}"
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
        Sid = "AllowLambdaToPullImageFromECR"
        Effect = "Allow"
        Action = [
          "ecr:GetAuthorizationToken",
          "ecr:BatchGetImage",
          "ecr:BatchCheckLayerAvailability"
        ]
        Resource = "${var.ecr_arn}"
      },
      # {
      #   Sid = "AllowLambdaToSendStatusToStepFunctions"
      #   Effect = "Allow"
      #   Action = [
      #     "states:SendTaskSuccess",
      #     "states:SendTaskFailure"
      #   ]
      #   Resource = "${var.sfn_arn}"
      # },
      {
        Sid    = "AllowLambdaToUseKMSKey"
        Effect = "Allow"
        Action = [
          "kms:Encrypt",
          "kms:Decrypt",
          "kms:GenerateDataKey"
        ]
        Resource = "${var.kms_arn}"
      }
    ]
  })
}

