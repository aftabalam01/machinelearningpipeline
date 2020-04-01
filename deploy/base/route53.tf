/*
# route53 zone
# Reusing ea.tableausoftware.com domain
data "aws_route53_zone" "eats-main" {
  zone_id = "Z35V0N9X42S9SN"
}

# create new cert for eats
resource "aws_acm_certificate" "eats_cert" {

  domain_name       = "*.${var.domain_name}"
  validation_method = "DNS"
  //subject_alternative_names = ["*.${var.domain_name}"]

  tags = {
    Creator     = "${var.TAG_CREATOR}"
    Environment = "${var.TAG_ENVIRONMENT}"
    DeptCode    = "${var.TAG_DEPT}"
    Group       = "${var.TAG_GROUP}"
    Application = "${var.TAG_APPLICATION}"
    Owner       = "${var.TAG_OWNER}"
    Name        = "eats_domain_cert"
  
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_validation" {
  name    = "${aws_acm_certificate.eats_cert.domain_validation_options.0.resource_record_name}"
  type    = "${aws_acm_certificate.eats_cert.domain_validation_options.0.resource_record_type}"
  zone_id = "${data.aws_route53_zone.eats-main.zone_id}"
  records = ["${aws_acm_certificate.eats_cert.domain_validation_options.0.resource_record_value}"]
  ttl     = 60
}

resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = "${aws_acm_certificate.eats_cert.arn}"
  validation_record_fqdns = ["${aws_route53_record.cert_validation.fqdn}"]
}
*/