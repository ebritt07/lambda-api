output "api_gateway_lambda_collection_id" {
  value = aws_api_gateway_rest_api.lambda_collection.id
}

output "api_gateway_lambda_collection_execution_arn" {
  value = aws_api_gateway_rest_api.lambda_collection.execution_arn
}

output "api_gateway_lambda_collection_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.lambda_collection.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.lambda_collection.stage_name}"
}
