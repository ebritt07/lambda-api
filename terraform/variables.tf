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
