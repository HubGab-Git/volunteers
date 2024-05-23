resource "aws_ecr_repository" "lambdas" {
  for_each = local.lambdas
  name     = each.key

  image_scanning_configuration {
    scan_on_push = false
  }
}
