terraform {
  required_version = "~> 1.8.3"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.49.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6.1"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4.2"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  default_tags {
    tags = {
      Project = "volunteers"
    }
  }
}