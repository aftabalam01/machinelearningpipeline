variable "tags" {
  description = "A mapping of tags to assign to all resources"
  default     = {}
}

variable "AWS_REGION" {
  type    = string
  default = "us-west-2"
}

variable "account_id" {
  type    = string
}

variable "api_environment" {
  type= string
  default="stage"
}
