variable "region" {
  type    = string
  default = "us-east-1"
}

variable "zip_path" {
  description = "Path to store lambda zip files."
  type        = string
  default     = "zip_artifacts"
}

variable "aws_account_id" {
  type = string
}

variable "service_name" {
  type = string
}

variable "environment" {
  type        = string
  description = "Environment name (e.g., dev, staging, prod)."
}

variable "lambda_source_dir" {
  type        = string
  default     = null
  description = "Directory containing lambda code (will be zipped as a single artifact)."
}

variable "dynamodb_table_name" {
  type        = string
  description = "Base DynamoDB table name (service/environment prefix will be applied)."
}

variable "dynamodb_hash_key" {
  type        = string
  description = "Hash key attribute name for the DynamoDB table."
}

variable "dynamodb_range_key" {
  type        = string
  default     = null
  description = "Optional range key attribute name for the DynamoDB table."
}

variable "dynamodb_attributes" {
  type = list(object({
    name = string
    type = string
  }))
  description = "Attribute definitions for the DynamoDB table."
}

variable "dynamodb_billing_mode" {
  type        = string
  default     = "PAY_PER_REQUEST"
  description = "DynamoDB billing mode (PAY_PER_REQUEST or PROVISIONED)."
}

variable "dynamodb_read_capacity" {
  type        = number
  default     = null
  description = "Read capacity units (required for PROVISIONED)."
}

variable "dynamodb_write_capacity" {
  type        = number
  default     = null
  description = "Write capacity units (required for PROVISIONED)."
}

variable "dynamodb_ttl" {
  type = object({
    attribute_name = string
    enabled        = bool
  })
  default     = null
  description = "Optional TTL configuration for the DynamoDB table."
}

variable "dynamodb_global_secondary_indexes" {
  type = list(object({
    name               = string
    hash_key           = string
    range_key          = optional(string)
    projection_type    = optional(string)
    non_key_attributes = optional(list(string))
    read_capacity      = optional(number)
    write_capacity     = optional(number)
  }))
  default     = []
  description = "Optional list of global secondary indexes."
}
