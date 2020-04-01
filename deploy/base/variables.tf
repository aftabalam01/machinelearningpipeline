variable "AWS_REGION" {
  type    = string
  default = "us-west-2"
}

variable "AWS_PROFILE" {
  type    = string
  default = "saml"
}

variable "TAG_CREATOR" {
  type = string
}

variable "TAG_ENVIRONMENT" {
  type    = string
  default = "dev"
}

variable "TAG_DEPT" {
  type = string
}

variable "TAG_GROUP" {
  type = string
}

variable "TAG_APPLICATION" {
  type = string
}

variable "TAG_OWNER" {
  type = string
}

variable "domain_name" {
    type=string
    default="ea.tableausoftware.com"
}

variable "public_dir" {
  description = "Directory in S3 Bucket from which to serve public files (no leading or trailing slashes)"
  default     = "public"
}
