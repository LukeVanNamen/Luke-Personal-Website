terraform {
    required_providers {
        aws = {
            version = ">=4.9.0"
            source = "hashicorp/aws"
        }
    }
}
provider "aws" {
    profile = "website-dev"
    # access_key
    # secret_key
    region = "us-east-2"
}