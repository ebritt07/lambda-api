data "aws_caller_identity" "current" {}

locals {
  frontend_dist_dir   = "${path.root}/../typescript/dist"
  frontend_dist_files = fileset(local.frontend_dist_dir, "**")
  frontend_mime_types = {
    ".css"  = "text/css"
    ".html" = "text/html"
    ".js"   = "application/javascript"
    ".json" = "application/json"
    ".map"  = "application/json"
    ".png"  = "image/png"
    ".svg"  = "image/svg+xml"
    ".txt"  = "text/plain"
  }
}

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

resource "aws_s3_object" "frontend_dist_files" {
  for_each = { for file in local.frontend_dist_files : file => file }

  bucket = aws_s3_bucket.frontend_artifacts.id
  key    = each.value
  source = "${local.frontend_dist_dir}/${each.value}"
  etag   = filemd5("${local.frontend_dist_dir}/${each.value}")

  content_type = lookup(
    local.frontend_mime_types,
    try(regex("\\.[^.]+$", each.value), ""),
    "application/octet-stream"
  )
}
