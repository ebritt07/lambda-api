locals {
  zip_output_dir = "${path.root}/zip_artifacts"

  cognito_authorizer_name            = "ebritt07-authorizer"
  cognito_resource_server_identifier = "ebritt07.click"
  cognito_bike_modify_scope          = "ebritt07.click/bike.modify"
}
