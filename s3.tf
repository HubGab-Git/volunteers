# kics-scan disable=42bb6b7f-6d54-4428-b707-666f669d94fb

resource "aws_s3_bucket" "website_bucket" {
  bucket = "${local.name}-website-bucket-${random_string.random.result}"
}

resource "aws_s3_object" "website_files" {
  bucket = aws_s3_bucket.website_bucket.id
  key    = "styles.css"
  source = "./website/styles.css"
  etag   = filemd5("./website/styles.css")

  # content_type = local.mime_types
}

resource "aws_s3_object" "index_html" {
  bucket = aws_s3_bucket.website_bucket.id
  key    = "index.html"
  #source = local_file.index_html.filename
  #etag   = filemd5(local_file.index_html.filename)
  content = local_file.index_html.content

  content_type = "text/html"

  #depends_on = [ local_file.index_html ]
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

resource "aws_s3_bucket_public_access_block" "website_bucket" {
  bucket = aws_s3_bucket.website_bucket.id

  block_public_acls = false
  # kics-scan ignore-line
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "website_bucket" {
  bucket = aws_s3_bucket.website_bucket.id
  policy = data.aws_iam_policy_document.website_bucket.json
}
