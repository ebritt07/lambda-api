module "bicycle_lambda" {
  source = "./modules/bicycle_lambda"

  function_name      = "bicycle_lambda"
  runtime            = "python3.12"
  source_dir         = "${path.root}/../python"
  dynamodb_table_arn = aws_dynamodb_table.bikes.arn
}
