variable "function_name" {
  type    = string
  default = "bicycle_lambda"
}

variable "handler" {
  type    = string
  default = "src.main.lambdas.bicycle_lambda.bicycle_lambda.handler"
}

variable "runtime" {
  type    = string
  default = "python3.12"
}

variable "source_dir" {
  type = string
}

variable "zip_output_dir" {
  type    = string
}

variable "dynamodb_table_arn" {
  type = string
}

variable "memory_size" {
  type    = number
  default = 128
}

variable "timeout" {
  type    = number
  default = 10
}

variable "env" {
  type    = string
  default = "dev"
}
