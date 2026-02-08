output "lambda_function_arn" {
  value = aws_lambda_function.bicycle_lambda.arn
}

output "dynamodb_table_arn" {
  value = aws_dynamodb_table.main.arn
}
