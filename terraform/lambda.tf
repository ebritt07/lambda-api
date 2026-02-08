data "archive_file" "bicycle_lambda" {
  type        = "zip"
  source_dir  = local.lambda_source_dir
  output_path = local.lambda_zip
}

resource "aws_lambda_function" "bicycle_lambda" {
  function_name = "${var.service_name}-${var.environment}-bicycle_lambda"
  role          = aws_iam_role.bicycle_lambda.arn
  handler       = "bicycle_lambda.handler"
  runtime       = "python3.13"

  filename         = data.archive_file.bicycle_lambda.output_path
  source_code_hash = data.archive_file.bicycle_lambda.output_base64sha256

  memory_size = 128
  timeout     = 10
}
