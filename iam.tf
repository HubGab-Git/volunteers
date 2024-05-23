resource "aws_iam_role" "lambda_exec" {
  name               = "serverless_lambda"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole",
    aws_iam_policy.get_secret_value.arn
  ]
}

resource "aws_iam_role" "cloudwatch" {
  name               = "api_gateway_cloudwatch_global"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy" "cloudwatch" {
  name   = "default"
  role   = aws_iam_role.cloudwatch.id
  policy = data.aws_iam_policy_document.cloudwatch.json
}

resource "aws_iam_policy" "get_secret_value" {
  name   = "get_secret_value"
  policy = data.aws_iam_policy_document.get_secret_value.json
}