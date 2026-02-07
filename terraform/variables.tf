variable "region" {
  type    = string
  default = "us-east-1"
}

variable "zip_path" {
  description = "path to store lambda zip files"
  type        = string
  default     = "zip_artifacts"
}

variable "aws_account_id" {
  type = string
}

variable "service_name" {
  type = string
}