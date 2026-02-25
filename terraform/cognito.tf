resource "aws_cognito_resource_server" "api" {
  user_pool_id = element(split("/", local.cognito_user_pool_arn), 1)
  identifier   = local.cognito_resource_server_identifier
  name         = "ebritt07 API"

  scope {
    scope_name        = "bike.modify"
    scope_description = "Create, update, and delete bike records"
  }
}
