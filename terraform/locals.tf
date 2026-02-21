locals {
  zip_output_dir = "${path.root}/zip_artifacts"

  api_gateway_contract = jsondecode(file("${path.root}/${var.api_gateway_contract_path}"))

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
      for prefix in keys(var.api_gateway_route_lambda_map) :
      format("%05d|%s", length(prefix), prefix)
    ])) :
    split("|", pair)[1]
  ]

  api_gateway_unknown_lambda_keys = setsubtract(
    toset(values(var.api_gateway_route_lambda_map)),
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
    path_name => merge(path_item, {
      for method_name, method_value in path_item :
      method_name => (
        contains(local.api_gateway_http_methods, lower(method_name))
        ? merge(
          method_value,
          {
            "x-amazon-apigateway-integration" = {
              type                 = "aws_proxy"
              httpMethod           = "POST"
              payloadFormatVersion = "1.0"
              uri = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${
                local.api_gateway_lambda_targets[
                  var.api_gateway_route_lambda_map[
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
        : method_value
      )
    })
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
