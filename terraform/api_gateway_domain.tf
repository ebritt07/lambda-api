locals {
  api_custom_domain_name = "api.${var.root_domain_name}"
}

resource "aws_api_gateway_domain_name" "lambda_collection" {
  domain_name              = local.api_custom_domain_name
  regional_certificate_arn = var.root_domain_certificate_arn

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_base_path_mapping" "lambda_collection" {
  api_id      = aws_api_gateway_rest_api.lambda_collection.id
  stage_name  = aws_api_gateway_stage.lambda_collection.stage_name
  domain_name = aws_api_gateway_domain_name.lambda_collection.domain_name
}

data "aws_route53_zone" "api_root" {
  name         = "${var.root_domain_name}."
  private_zone = false
}

resource "aws_route53_record" "lambda_collection_api_domain" {
  zone_id = data.aws_route53_zone.api_root.zone_id
  name    = local.api_custom_domain_name
  type    = "A"

  alias {
    name                   = aws_api_gateway_domain_name.lambda_collection.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.lambda_collection.regional_zone_id
    evaluate_target_health = false
  }
}
