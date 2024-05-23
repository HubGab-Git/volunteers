output "website_endpoint" {
  value = "http://${aws_s3_bucket_website_configuration.website_bucket.website_endpoint}"
}

output "website_api_endpoint" {
  value = aws_api_gateway_deployment.website_api_deployment.invoke_url
}