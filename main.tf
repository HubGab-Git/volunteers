provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "website_bucket" {
  bucket = "XXXXXXXXXXwebsite-bucket"
  acl    = "public-read"

  website {
    index_document = "index.html"
    error_document = "error.html"
  }
}

resource "aws_s3_bucket_object" "website_files" {
  for_each = fileset("./website", "**/*")

  bucket = aws_s3_bucket.website_bucket.id
  key    = each.value
  source = "./website/${each.value}"
  etag   = filemd5("./website/${each.value}")
  acl    = "public-read"

  content_type = lookup(local.mime_types, split(".", each.value)[length(split(".", each.value)) - 1], "application/octet-stream")
}

locals {
  mime_types = {
    html = "text/html"
    js   = "application/javascript"
    css  = "text/css"
    png  = "image/png"
    jpg  = "image/jpeg"
    json = "application/json"
  }
}

output "website_endpoint" {
  value = aws_s3_bucket.website_bucket.website_endpoint
}
