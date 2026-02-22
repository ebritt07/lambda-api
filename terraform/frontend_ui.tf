locals {
  org_name                  = "ebritt07"
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

data "aws_iam_policy_document" "frontend_artifacts_amplify_read" {
  statement {
    sid = "AllowAmplifyManualDeployRead"

    principals {
      type        = "Service"
      identifiers = ["amplify.amazonaws.com"]
    }

    actions = [
      "s3:GetBucketLocation",
      "s3:ListBucket",
    ]

    resources = [
      aws_s3_bucket.frontend_artifacts.arn,
    ]
  }

  statement {
    sid = "AllowAmplifyManualDeployObjectRead"

    principals {
      type        = "Service"
      identifiers = ["amplify.amazonaws.com"]
    }

    actions = [
      "s3:GetObject",
      "s3:GetObjectVersion",
    ]

    resources = [
      "${aws_s3_bucket.frontend_artifacts.arn}/*",
    ]
  }
}

resource "aws_s3_bucket_policy" "frontend_artifacts_amplify_read" {
  bucket = aws_s3_bucket.frontend_artifacts.id
  policy = data.aws_iam_policy_document.frontend_artifacts_amplify_read.json
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
