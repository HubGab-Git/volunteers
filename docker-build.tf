resource "null_resource" "build_push" {
  for_each = local.lambdas
  triggers = {
    detect_docker_source_changes = sha256(file("${local.lambdas_path}/${each.key}/app.py"))
    docker_image_tag             = each.value
  }

  provisioner "local-exec" {
    command = file("${path.module}/bash/docker-build-${each.key}.sh")
  }
  depends_on = [local_file.build_push]
}