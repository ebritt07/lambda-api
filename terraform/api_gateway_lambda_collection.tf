resource "aws_api_gateway_rest_api" "lambda_collection" {
  name = var.api_gateway_name
  body = jsonencode(local.api_gateway_openapi_document)

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  lifecycle {
    precondition {
      condition     = length(local.api_gateway_unknown_lambda_keys) == 0
      error_message = "api_gateway_route_lambda_map references undefined lambda keys."
    }
    precondition {
      condition     = length(local.api_gateway_unmapped_paths) == 0
      error_message = "Some OpenAPI paths do not match any api_gateway_route_lambda_map prefix."
    }
  }
}

resource "aws_lambda_permission" "api_gateway_invoke" {
  for_each = toset([
    for key in values(var.api_gateway_route_lambda_map) :
    key if contains(keys(local.api_gateway_lambda_targets), key)
  ])

  statement_id  = "AllowExecutionFromApiGateway${replace(title(each.key), "_", "")}"
  action        = "lambda:InvokeFunction"
  function_name = local.api_gateway_lambda_targets[each.key].lambda_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.lambda_collection.execution_arn}/*/*"
}

resource "aws_api_gateway_deployment" "lambda_collection" {
  rest_api_id = aws_api_gateway_rest_api.lambda_collection.id

  triggers = {
    redeployment = sha1(jsonencode(local.api_gateway_openapi_document))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_lambda_permission.api_gateway_invoke]
}

resource "aws_api_gateway_stage" "lambda_collection" {
  rest_api_id   = aws_api_gateway_rest_api.lambda_collection.id
  deployment_id = aws_api_gateway_deployment.lambda_collection.id
  stage_name    = var.env
}
