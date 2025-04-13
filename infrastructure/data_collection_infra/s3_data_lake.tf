


resource "aws_s3_bucket" "jikan_data_lake" {
  bucket = var.s3_data_lake_name
}


resource "aws_s3_bucket_public_access_block" "name" {
  bucket = aws_s3_bucket.jikan_data_lake.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}


resource "aws_s3_bucket_server_side_encryption_configuration" "jika_data_lake_encryption_config" {
  bucket = aws_s3_bucket.jikan_data_lake.id

  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.anime_kms_key.arn
    }
  }
}

resource "aws_s3_bucket_policy" "jikan_data_lake_bucket_policy" {
  bucket = aws_s3_bucket.jikan_data_lake.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "JikanS3DataLakePolicy"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "${aws_s3_bucket.jikan_data_lake.arn}",
          "${aws_s3_bucket.jikan_data_lake.arn}/*"
        ]
      },
      {
        Sid = "AllowGlueAccessToS3"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
        Action = [
          "s3:ListBucket",
          "s3:GetObject"
        ]
        Resource = [
          "${aws_s3_bucket.jikan_data_lake.arn}",
          "${aws_s3_bucket.jikan_data_lake.arn}/*"
        ]
      }
    ]
  })
}

