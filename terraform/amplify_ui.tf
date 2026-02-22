resource "aws_amplify_app" "frontend" {
  name     = "${local.org_name}-frontend-${var.env}"
  platform = "WEB"
}

resource "aws_amplify_branch" "frontend_main" {
  app_id            = aws_amplify_app.frontend.id
  branch_name       = "main"
  enable_auto_build = false
}

resource "aws_amplify_domain_association" "frontend" {
  count = var.root_domain_name != "" ? 1 : 0

  app_id      = aws_amplify_app.frontend.id
  domain_name = var.root_domain_name

  sub_domain {
    branch_name = aws_amplify_branch.frontend_main.branch_name
    prefix      = ""
  }
}

resource "null_resource" "trigger_manual_deploy" {
  triggers = {
    s3_object_etag = local.frontend_dist_etag_hash
  }

  provisioner "local-exec" {
    command = <<-EOT
      aws amplify start-deployment --app-id ${aws_amplify_app.frontend.id} --branch-name ${aws_amplify_branch.frontend_main.branch_name} --source-url s3://${aws_s3_bucket.frontend_artifacts.bucket}/ --source-url-type BUCKET_PREFIX --region ${var.region}
    EOT
  }

  depends_on = [
    aws_s3_object.frontend_dist_files,
    aws_s3_bucket_policy.frontend_artifacts_amplify_read
  ]
}
