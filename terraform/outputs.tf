output "api_gateway_lambda_collection_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.lambda_collection.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.lambda_collection.stage_name}"
}

output "api_gateway_custom_domain_invoke_url" {
  value = "https://${aws_api_gateway_domain_name.lambda_collection.domain_name}"
}

output "ui_url" {
  value = "https://${var.root_domain_name}"
}
