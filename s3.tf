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