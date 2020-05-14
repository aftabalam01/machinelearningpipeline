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

provider "random"{
  version = "~> 2.1.0"
}
terraform {
  backend "s3" {
  }
}

# get the account details of caller as accountid is part of most of arn
data "aws_caller_identity" "current" {}

#output "account_id" {
#  value = "${data.aws_caller_identity.current.account_id}"
#}
module "assignment1" {
  source              = "./Assignment1"

  AWS_REGION          = "${var.AWS_REGION}"
  account_id          = "${data.aws_caller_identity.current.account_id}"
  tags={Creator         = "${var.TAG_CREATOR}"
  Environment          = "${var.TAG_ENVIRONMENT}"
  DeptCode                 = "${var.TAG_DEPT}"
  Group                = "${var.TAG_GROUP}"
  Application          = "${var.TAG_APPLICATION}"
  Owner                = "${var.TAG_OWNER}"}
}
