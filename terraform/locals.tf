locals {
  lambda_source_dir = coalesce(var.lambda_source_dir, "${path.module}/../src/main/bicycle_lambda")
  lambda_zip        = "${var.zip_path}/bicycle_lambda.zip"
}
