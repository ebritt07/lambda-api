resource "aws_dynamodb_table" "bikes" {
  name         = "BIKES"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  attribute {
    name = "owner_id"
    type = "S"
  }

  global_secondary_index {
    name            = "owner_id-index"
    hash_key        = "owner_id"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "users" {
  name         = "USERS"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }
}
