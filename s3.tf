resource "aws_s3_bucket" "website_bucket" {
  bucket = "${local.name}-website-bucket-${random_string.random.result}"
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

resource "aws_s3_bucket_website_configuration" "website_bucket" {
  bucket = aws_s3_bucket.website_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}