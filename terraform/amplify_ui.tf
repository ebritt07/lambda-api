module "amplify_s3_deployment" {
  source = "JetBrains/amplify/aws//modules/terraform-aws-amplify-static-website-deployment-from-s3"

  app_name    = "${local.org_name}-frontend-${var.env}"
  branch_name = "main"

  s3_details = {
    bucket = aws_s3_bucket.frontend_artifacts.bucket
  }

  depends_on = [
    aws_s3_object.frontend_dist_files
  ]
}
