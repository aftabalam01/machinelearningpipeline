# Configure Terragrunt to use DynamoDB for locking

# Configure Terragrunt to automatically store tfstate files in S3
# read this to know more about terragrunt https://github.com/gruntwork-io/terragrunt

remote_state {
  backend = "s3"
  config ={
    encrypt = true
    bucket = "eats-service-terraform-remote-state"
    key = "dev/terraform.tfstate"
    region = "us-west-2"
    dynamodb_table = "eats-service-terraform-lock-table"

    s3_bucket_tags = {
      Owner = "Eats"
      Name  = "Eats_Terraform_remote_state_bucket"
      DeptCode = "460"
      Creator = "eats@tableau.com"
      Description = "Table to manage eats terrformlock"
      Group = "eats"
      Application = "eats_service"
      Environment = "dev"
      }

    dynamodb_table_tags= {
      Owner = "Eats"
      Name  = "eats-service-terraform-lock-table"
      DeptCode = "460"
      Creator = "eats@tableau.com"
      Description = "Table to manage eats terrformlock"
      Group = "eats"
      Application = "eats_service"
      Environment = "dev"
      }
    }
}

terraform {
  source = "${get_terragrunt_dir()}/../terraform/"

  extra_arguments "custom_vars" {
    commands = [
      "apply",
      "plan",
      "import",
      "push",
      "refresh",
      "destroy"
    ]

    # With the get_terragrunt_dir() function, you can use relative paths!
    arguments = [
      "-var-file=${get_terragrunt_dir()}/../terraform/common.tfvars",
      "-var-file=dev.tfvars"
    ]
  }
  # Force Terraform to keep trying to acquire a lock for
  # up to 20 minutes if someone else already has the lock
  extra_arguments "retry_lock" {
    commands  = get_terraform_commands_that_need_locking()
    arguments = ["-lock-timeout=20m"]
  }
}

inputs = {
}