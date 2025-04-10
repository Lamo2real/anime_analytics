


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


