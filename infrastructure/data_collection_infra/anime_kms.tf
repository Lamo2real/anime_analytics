data "aws_caller_identity" "current_dev" {}

resource "aws_kms_key" "anime_kms_key" {
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  enable_key_rotation      = true
  description              = "this is the key used for s3 & glue"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "jikan-data-key-id"
    Statement = [
      {
        Sid    = "S3PermissionsToKMS"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current_dev.account_id}:user/*"
        }
        Action   = "kms:*"
        Resource = "*"
      }
    ]
  })
}

