output "api_gateway_lambda_collection_id" {
  value = aws_api_gateway_rest_api.lambda_collection.id
}

output "api_gateway_lambda_collection_execution_arn" {
  value = aws_api_gateway_rest_api.lambda_collection.execution_arn
}

output "api_gateway_lambda_collection_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.lambda_collection.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.lambda_collection.stage_name}"
}

output "api_gateway_custom_domain_name" {
  value = aws_api_gateway_domain_name.lambda_collection.domain_name
}

output "api_gateway_custom_domain_invoke_url" {
  value = "https://${aws_api_gateway_domain_name.lambda_collection.domain_name}"
}

output "frontend_artifacts_bucket_name" {
  value = aws_s3_bucket.frontend_artifacts.bucket
}

output "frontend_dist_zip_s3_key" {
  value = aws_s3_object.frontend_dist_zip.key
}
