variable "region" {
  type    = string
  default = "us-east-1"
}

variable "env" {
  type    = string
  default = "dev"
}

variable "zip_output_dir" {
  type = string
  default = "zip_artifacts"
}

variable "dynamodb_read_policy_arn" {
  type    = string
  default = ""
}

variable "dynamodb_readwrite_policy_arn" {
  type    = string
  default = ""
}

variable "s3_read_policy_arn" {
  type    = string
  default = ""
}
