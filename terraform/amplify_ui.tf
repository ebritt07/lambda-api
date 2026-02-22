resource "aws_amplify_app" "frontend" {
  name     = "${local.org_name}-frontend-${var.env}"
  platform = "WEB"
}

resource "aws_amplify_branch" "frontend_main" {
  app_id      = aws_amplify_app.frontend.id
  branch_name = "main"
}

resource "aws_amplify_domain_association" "frontend" {
  count = var.local_domain_name != "" ? 1 : 0

  app_id      = aws_amplify_app.frontend.id
  domain_name = var.local_domain_name

  sub_domain {
    branch_name = aws_amplify_branch.frontend_main.branch_name
    prefix      = ""
  }
}

resource "terraform_data" "amplify_frontend_deployment" {
  triggers_replace = [
    local.frontend_dist_etag_hash
  ]

  provisioner "local-exec" {
    command = "aws amplify start-deployment --app-id ${aws_amplify_app.frontend.id} --branch-name ${aws_amplify_branch.frontend_main.branch_name} --source-url s3://${aws_s3_bucket.frontend_artifacts.bucket}/ --source-url-type BUCKET_PREFIX --region ${var.region}"
  }

  depends_on = [
    aws_s3_object.frontend_dist_files
  ]
}
