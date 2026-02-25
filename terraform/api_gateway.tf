locals {
  api_gateway_contract_path = "openapi/openapi.json"

  api_gateway_contract = jsondecode(file("${path.root}/${local.api_gateway_contract_path}"))

  api_gateway_lambda_targets = {
    "/admin" = {
      lambda_arn  = module.admin_lambda.lambda_arn
      lambda_name = module.admin_lambda.lambda_name
    }
    "/bike" = {
      lambda_arn  = module.bicycle_lambda.lambda_arn
      lambda_name = module.bicycle_lambda.lambda_name
    }
  }

  api_gateway_matching_prefixes = {
    for path_name in keys(local.api_gateway_contract.paths) :
    path_name => [
      for prefix in keys(local.api_gateway_lambda_targets) :
      prefix if startswith(path_name, prefix)
    ]
  }

  api_gateway_unmapped_paths = [
    for path_name, prefixes in local.api_gateway_matching_prefixes :
    path_name if length(prefixes) == 0
  ]

  # Resolve each API path to the most specific configured prefix.
  api_gateway_path_target_prefix = {
    for path_name, prefixes in local.api_gateway_matching_prefixes :
    path_name => one([
      for prefix in prefixes :
      prefix if length(prefix) == max([
        for candidate in prefixes :
        length(candidate)
      ]...)
    ])
    if length(prefixes) > 0
  }

  api_gateway_http_methods = ["get", "put", "post", "delete", "patch", "head", "options"]

  api_gateway_components = lookup(local.api_gateway_contract, "components", {})

  api_gateway_security_schemes = lookup(local.api_gateway_components, "securitySchemes", {})
  cognito_user_pool_arn        = "arn:aws:cognito-idp:us-east-1:862315107606:userpool/us-east-1_6IDvYI8kL"

  api_gateway_authorized_security_schemes = merge(
    local.api_gateway_security_schemes,
    local.cognito_user_pool_arn == "" ? {} : {
      (local.cognito_authorizer_name) = merge(
        lookup(local.api_gateway_security_schemes, local.cognito_authorizer_name, {}),
        {
          "type"                         = "apiKey"
          "name"                         = "Authorization"
          "in"                           = "header"
          "x-amazon-apigateway-authtype" = "cognito_user_pools"
          "x-amazon-apigateway-authorizer" = {
            type         = "cognito_user_pools"
            providerARNs = [local.cognito_user_pool_arn]
          }
        }
      )
    }
  )

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
                  local.api_gateway_path_target_prefix[path_name]
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
    components = merge(
      local.api_gateway_components,
      {
        securitySchemes = local.api_gateway_authorized_security_schemes
      }
    )
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
      condition     = length(local.api_gateway_unmapped_paths) == 0
      error_message = "Some OpenAPI paths do not match any local.api_gateway_lambda_targets path_prefix."
    }
  }
}

resource "aws_lambda_permission" "api_gateway_invoke" {
  for_each = local.api_gateway_lambda_targets

  statement_id  = "AllowExecutionFromApiGateway${replace(title(each.value.lambda_name), "_", "")}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.lambda_name
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
