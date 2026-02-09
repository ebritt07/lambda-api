module "bicycle_lambda" {
  source = "./modules/dynamo_lambda"

  function_name      = "bicycle_lambda"
  runtime            = "python3.12"
  source_dir         = "${path.root}/../python"
  zip_output_dir     = "${path.root}/${var.zip_output_dir}"
  dynamodb_table_arn = aws_dynamodb_table.bikes.arn
  policy_arns = compact([
    var.dynamodb_read_policy_arn,
    var.dynamodb_readwrite_policy_arn,
    var.s3_read_policy_arn
  ])
}
