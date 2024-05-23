resource "aws_lambda_function" "this" {
  for_each      = local.lambdas
  image_uri     = "${aws_ecr_repository.lambdas[each.key].repository_url}:${each.value}"
  function_name = each.key
  role          = aws_iam_role.lambda_exec.arn
  package_type  = "Image"

  vpc_config {
    subnet_ids         = [aws_subnet.private[0].id]
    security_group_ids = [aws_security_group.lambda_rds.id]
  }

  environment {
    variables = {
      DBNAME = aws_db_instance.db.db_name
      HOST   = aws_db_instance.db.address
      PORT   = aws_db_instance.db.port
      SECRET = aws_db_instance.db.master_user_secret[0].secret_arn
    }
  }
  depends_on = [local_file.build_push, null_resource.build_push]
}
