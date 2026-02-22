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

variable "frontend_source_directory" {
  description = "The local path to the frontend files uploaded to S3."
  type        = string
  default     = "../typescript/dist"
}

variable "root_domain_name" {
  type    = string
  default = ""
}

variable "root_domain_certificate_arn" {
  type    = string
  default = ""
}

variable "local_domain_name" {
  type    = string
  default = ""
}
