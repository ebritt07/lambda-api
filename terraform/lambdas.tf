module "bicycle_lambda" {
  source = "./modules/dynamo_lambda"

  function_name      = "bicycle_lambda"
  handler            = "src.main.lambdas.bicycle_lambda.bicycle_lambda.handler"
  runtime            = "python3.12"
  source_dir         = "${path.root}/../python"
  zip_output_dir     = local.zip_output_dir
  dynamodb_table_arns = [
    aws_dynamodb_table.bikes.arn
  ]
  env = var.env
}

module "admin_lambda" {
  source = "./modules/dynamo_lambda"

  function_name      = "admin_lambda"
  handler            = "src.main.lambdas.admin_lambda.admin_lambda.handler"
  runtime            = "python3.12"
  source_dir         = "${path.root}/../python"
  zip_output_dir     = local.zip_output_dir
  dynamodb_table_arns = [
    aws_dynamodb_table.bikes.arn,
    aws_dynamodb_table.users.arn
  ]
  env = var.env
}
