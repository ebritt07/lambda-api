resource "aws_dynamodb_table" "main" {
  name         = "${var.service_name}-${var.environment}-${var.dynamodb_table_name}"
  hash_key     = var.dynamodb_hash_key
  range_key    = var.dynamodb_range_key
  billing_mode = var.dynamodb_billing_mode

  read_capacity  = var.dynamodb_read_capacity
  write_capacity = var.dynamodb_write_capacity

  dynamic "attribute" {
    for_each = var.dynamodb_attributes
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }

  dynamic "ttl" {
    for_each = var.dynamodb_ttl == null ? [] : [var.dynamodb_ttl]
    content {
      attribute_name = ttl.value.attribute_name
      enabled        = ttl.value.enabled
    }
  }

  dynamic "global_secondary_index" {
    for_each = var.dynamodb_global_secondary_indexes
    content {
      name               = global_secondary_index.value.name
      hash_key           = global_secondary_index.value.hash_key
      range_key          = try(global_secondary_index.value.range_key, null)
      projection_type    = try(global_secondary_index.value.projection_type, "ALL")
      non_key_attributes = try(global_secondary_index.value.non_key_attributes, null)
      read_capacity      = try(global_secondary_index.value.read_capacity, null)
      write_capacity     = try(global_secondary_index.value.write_capacity, null)
    }
  }
}
