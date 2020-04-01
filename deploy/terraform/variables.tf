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

variable "vpc_stage" {
  type = string
  default = "vpc-48f9452f"
}

variable "vpc_dev" {
  type = string
  default = "vpc-48f9452f"
}


variable "subnet_id_dev_1" {
  type = string
  default   = "subnet-3621d47f"
  }
variable "subnet_id_stage_1" {
  type = string
  default = "subnet-3621d47f"
}

variable "subnet_id_dev_2" {
  type = string
  default   = "subnet-00578467"
  }
variable "subnet_id_stage_2" {
  type = string
  default = "subnet-00578467"
}

variable "default_sg" {
  type=string
  default="sg-fb22fa83"
}

# eats service db

variable "db_port"{
  type = string
  default="5432"
}
variable "db_username" {
  type = string
}
variable "db_password" {
  type = string
  default=""
}
variable "db_name" {
  type = string
}

variable "db_min_capacity" {
  type = number
  default=2
}

variable "db_max_capacity" {
  type = number
  default=32
}


# Cloudwatch config


variable "toemail" {
  type= string
  default = "eats@tableau.com"
  description = "comma seperated string"
}

variable "ccemail" {
  type= string
  default = "eats@tableau.com"
  description = "comma seperated string"
}
variable "eats_default_email" {
  type= string
  default = "eats@tableau.com"
  description = "comma seperated string"
}

variable "cluster_name" {
  type=string
  default="eats-service"
  description="eats service and UI ecs cluster"
}

variable "task_cpu" {
  type = number
  default=1024
}

variable "task_memory" {
  type = number
  default=2048
}

variable "instance_key_name" {
    type=string
    default="eats-performance_key"
}


variable "instance_type" {
    type=string
    default="t3.medium"
}

variable "instance_count_max" {
    type=string
    default="1"
}
variable "instance_count_min" {
    type=string
    default="1"
}
variable "instance_desired_count" {
    type=string
    default="1"
}

variable "tags" {
  description = "A mapping of tags to assign to all resources"
  default     = {}
}

variable "eats_service_ecr" {
  type=string
  default="212027156525.dkr.ecr.us-west-2.amazonaws.com/eats/service-layer"
}

variable "metadata_auto_conf_url"{
  type=string
}

variable "entity_id"{
  type=string
}
variable "branch"{
  type=string
}
variable "build"{
  type=string
}