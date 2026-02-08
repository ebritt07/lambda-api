locals {
  ddb_resource_arns = [
    aws_dynamodb_table.main.arn,
    "${aws_dynamodb_table.main.arn}/index/*"
  ]
}

data "aws_iam_policy_document" "lambda_assume" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "bicycle_lambda" {
  name               = "${var.service_name}-${var.environment}-lambda-bicycle_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume.json
}

resource "aws_iam_role_policy_attachment" "bicycle_lambda_basic" {
  role       = aws_iam_role.bicycle_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "ddb_read_write" {
  name = "${var.service_name}-${var.environment}-ddb-read-write"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid = "DynamoReadWrite"
        Effect = "Allow"
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:DescribeTable",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:DeleteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem"
        ]
        Resource = local.ddb_resource_arns
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "bicycle_lambda_ddb_read_write" {
  role       = aws_iam_role.bicycle_lambda.name
  policy_arn = aws_iam_policy.ddb_read_write.arn
}
