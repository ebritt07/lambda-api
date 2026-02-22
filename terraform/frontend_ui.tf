locals {
  org_name                 = "ebritt07"
  frontend_source_directory = abspath("${path.root}/${var.frontend_source_directory}")
  frontend_dist_files       = fileset(local.frontend_source_directory, "**")
  frontend_dist_etag_hash = sha1(join("", [
    for file in sort(local.frontend_dist_files) :
    filemd5("${local.frontend_source_directory}/${file}")
  ]))
}

resource "aws_s3_bucket" "frontend_artifacts" {
  bucket = "${local.org_name}-lambda-ui-artifacts-${var.env}"
}

resource "aws_s3_bucket_public_access_block" "frontend_artifacts" {
  bucket = aws_s3_bucket.frontend_artifacts.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_object" "frontend_dist_files" {
  for_each = local.frontend_dist_files

  bucket = aws_s3_bucket.frontend_artifacts.id
  key    = each.value
  source = "${local.frontend_source_directory}/${each.value}"
  etag   = filemd5("${local.frontend_source_directory}/${each.value}")
}
