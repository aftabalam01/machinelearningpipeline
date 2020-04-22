provider "aws" {
  region = "${var.AWS_REGION}"
  profile = "${var.AWS_PROFILE}"
  version = "~> 2.30"
}
provider "template" {
  version = "~> 2.1"
}

provider "archive"{
 version = "~> 1.2"
}

terraform {
  backend "s3" {
  }
}

# S3 bucket for data and model
resource "aws_s3_bucket" "uw-imt575" {
  bucket = "imt573-g3-databucket"
  acl = "private"

  tags =  "${merge(var.tags,map("Name" , "S3 source bucket for data and model"))}"
}

resource "aws_ecr_repository" "ecr_repo_data" {
  name = "g3/data-generation"
  tags = "${merge(var.tags,map("Name" , "data-generation"))}"

}

resource "aws_ecr_repository" "ecr_repo_model" {
  name = "g3/model"
  tags = "${merge(var.tags,map("Name" , "model"))}"

}