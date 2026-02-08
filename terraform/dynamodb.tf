resource "aws_dynamodb_table" "bikes" {
  name         = "${var.org_name}-bikes"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "ID"

  attribute {
    name = "ID"
    type = "S"
  }
}
