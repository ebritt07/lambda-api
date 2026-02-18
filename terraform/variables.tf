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
