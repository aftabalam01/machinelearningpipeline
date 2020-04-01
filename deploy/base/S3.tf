locals {
  eats_doc_website= "www.eats-infra-docs.com"
}

locals {
  public_dir_with_leading_slash = "${length(var.public_dir) > 0 ? "/${var.public_dir}" : ""}"
  static_website_routing_rules = <<EOF
[{
    "Condition": {
        "KeyPrefixEquals": "${var.public_dir}/${var.public_dir}/"
    },
    "Redirect": {
        "Protocol": "https",
        "HostName": "${var.domain_name}",
        "ReplaceKeyPrefixWith": "",
        "HttpRedirectCode": "301"
    }
}]
EOF
}

resource "aws_s3_bucket" "static_website" {
  bucket = "${local.eats_doc_website}"

  website {
    index_document = "index.html"
    error_document = "error.html"

    routing_rules = "${length(var.public_dir) > 0 ? local.static_website_routing_rules : ""}"
  }

  tags = {
    Creator     = "${var.TAG_CREATOR}"
    Environment = "${var.TAG_ENVIRONMENT}"
    DeptCode    = "${var.TAG_DEPT}"
    Group       = "${var.TAG_GROUP}"
    Application = "${var.TAG_APPLICATION}"
    Owner       = "${var.TAG_OWNER}"
    Name        = "${local.eats_doc_website}"
    Description = "eats static website"
  }
}

data "aws_iam_policy_document" "static_website_policy" {
  statement {
    sid       = "1"
    actions   = ["s3:*"]
    resources = ["${aws_s3_bucket.static_website.arn}${local.public_dir_with_leading_slash}/*"]
    effect = "Allow"
    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    condition {
      test = "IpAddress"
      variable = "aws:SourceIp"
      values = ["10.0.0.0/8","172.16.0.0/12","192.168.0.0/16"
    }
  }
}

resource "aws_s3_bucket_policy" "static_website_bucket_policy" {
  bucket = "${aws_s3_bucket.static_website.id}"
  policy = "${data.aws_iam_policy_document.static_website_policy.json}"
}

