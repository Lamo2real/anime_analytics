

resource "aws_s3_bucket" "infra_state" {
  bucket = var.aws_state_tracker
}

resource "aws_s3_bucket_versioning" "state_verions" {
  bucket = aws_s3_bucket.infra_state.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "state_encryption" {
  bucket = aws_s3_bucket.infra_state.id

  rule {
    bucket_key_enabled = true
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "anime_state_lifecycle" {
  bucket = aws_s3_bucket.infra_state.id

  rule {
    id = "terraform-states"
    status = "Enabled"

    filter {
      prefix = "infra/"
    }
    transition {
      days = 90
      storage_class = "STANDARD_IA"
    }
  }
}