locals {
  name = "volunteers"

  lambdas = {
    "db-schema"           = "0.0.4"
    "db-select"           = "0.0.3"
    "insert-example-data" = "0.0.4"
    "query-users"         = "0.0.12"
    "query-scout"         = "0.0.3"
  }

  lambdas_path = "${path.module}/lambda-code"
}