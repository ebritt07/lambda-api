locals {
  api_gateway_contract_path = "openapi/openapi.json"
  api_gateway_route_lambda_map = {
    "/admin" = "admin"
    "/bike"  = "bicycle"
  }

  api_gateway_contract = jsondecode(file("${path.root}/${local.api_gateway_contract_path}"))

  api_gateway_lambda_targets = {
    admin = {
      lambda_arn  = module.admin_lambda.lambda_arn
      lambda_name = module.admin_lambda.lambda_name
    }
    bicycle = {
      lambda_arn  = module.bicycle_lambda.lambda_arn
      lambda_name = module.bicycle_lambda.lambda_name
    }
  }

  api_gateway_route_prefixes_sorted = [
    for pair in reverse(sort([
      for prefix in keys(local.api_gateway_route_lambda_map) :
      format("%05d|%s", length(prefix), prefix)
    ])) :
    split("|", pair)[1]
  ]

  api_gateway_unknown_lambda_keys = setsubtract(
    toset(values(local.api_gateway_route_lambda_map)),
    toset(keys(local.api_gateway_lambda_targets))
  )

  api_gateway_unmapped_paths = [
    for path_name in keys(local.api_gateway_contract.paths) :
    path_name if length([
      for prefix in local.api_gateway_route_prefixes_sorted :
      prefix if startswith(path_name, prefix)
    ]) == 0
  ]

  api_gateway_http_methods = ["get", "put", "post", "delete", "patch", "head", "options"]

  api_gateway_paths_with_integration = {
    for path_name, path_item in local.api_gateway_contract.paths :
    path_name => merge(
      {
        for method_name, method_value in path_item :
        method_name => merge(
          method_value,
          {
            "x-amazon-apigateway-integration" = {
              type                 = "aws_proxy"
              httpMethod           = "POST"
              payloadFormatVersion = "1.0"
              uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${
                local.api_gateway_lambda_targets[
                  local.api_gateway_route_lambda_map[
                    [
                      for prefix in local.api_gateway_route_prefixes_sorted :
                      prefix if startswith(path_name, prefix)
                    ][0]
                  ]
                ].lambda_arn
              }/invocations"
            }
          }
        )
        if contains(local.api_gateway_http_methods, lower(method_name))
      },
      {
        for method_name, method_value in path_item :
        method_name => method_value
        if !contains(local.api_gateway_http_methods, lower(method_name))
      }
    )
  }

  api_gateway_openapi_document = {
    openapi = "3.0.1"
    info = {
      title   = var.api_gateway_name
      version = "1.0.0"
    }
    paths      = local.api_gateway_paths_with_integration
    components = lookup(local.api_gateway_contract, "components", {})
    "x-amazon-apigateway-request-validators" = {
      strict = {
        validateRequestBody       = true
        validateRequestParameters = true
      }
    }
    "x-amazon-apigateway-request-validator" = "strict"
  }
}

resource "aws_api_gateway_rest_api" "lambda_collection" {
  name = var.api_gateway_name
  body = jsonencode(local.api_gateway_openapi_document)

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  lifecycle {
    precondition {
      condition     = length(local.api_gateway_unknown_lambda_keys) == 0
      error_message = "local.api_gateway_route_lambda_map references undefined lambda keys."
    }
    precondition {
      condition     = length(local.api_gateway_unmapped_paths) == 0
      error_message = "Some OpenAPI paths do not match any local.api_gateway_route_lambda_map prefix."
    }
  }
}

resource "aws_lambda_permission" "api_gateway_invoke" {
  for_each = toset([
    for key in values(local.api_gateway_route_lambda_map) :
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
