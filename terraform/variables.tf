variable "region" {
  type    = string
  default = "us-east-1"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "api_gateway_name" {
  type    = string
  default = "api-lambda-collection"
}

variable "api_gateway_contract_path" {
  type    = string
  default = "openapi/openapi.json"
}

variable "api_gateway_route_lambda_map" {
  type = map(string)
  default = {
    "/admin" = "admin"
    "/bike"  = "bicycle"
  }
}
