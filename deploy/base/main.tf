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