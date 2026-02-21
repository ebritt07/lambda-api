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

variable "root_domain_name" {
  type    = string
  default = ""
}

variable "root_domain_certificate_arn" {
  type    = string
  default = ""
}
