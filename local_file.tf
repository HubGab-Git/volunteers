resource "local_file" "index_html" {
  content = templatefile(
    "${path.module}/templates/index.html.tpl",
    {
      api_gateway_url = aws_api_gateway_stage.website_api.invoke_url
    }
  )
  filename = "${path.module}/website/index.html"
}

resource "local_file" "build_push" {
  for_each = local.lambdas

  content = templatefile(
    "${path.module}/templates/docker-build.sh.tpl",
    {
      ecr_url   = aws_ecr_repository.lambdas[each.key].repository_url
      image_tag = each.value
      region    = data.aws_region.current.name
      ecr_reg   = replace(aws_ecr_repository.lambdas[each.key].repository_url, "/${each.key}", "")
      name      = each.key
    }
  )
  filename = "${path.module}/bash/docker-build-${each.key}.sh"
}
