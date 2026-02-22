data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "frontend_artifacts" {
  bucket = "lambda-ui-artifacts-${data.aws_caller_identity.current.account_id}-${var.env}"
}

resource "aws_s3_bucket_public_access_block" "frontend_artifacts" {
  bucket = aws_s3_bucket.frontend_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "frontend_dist_zip" {
  bucket = aws_s3_bucket.frontend_artifacts.id
  key    = "frontend/dist-${var.env}.zip"
  source = "${local.zip_output_dir}/frontend-dist.zip"
  etag   = filemd5("${local.zip_output_dir}/frontend-dist.zip")
}
