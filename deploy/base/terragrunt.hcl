# Configure Terragrunt to use DynamoDB for locking

# Configure Terragrunt to automatically store tfstate files in S3
# read this to know more about terragrunt https://github.com/gruntwork-io/terragrunt

remote_state {
  backend = "s3"
  config ={
    encrypt = true
    bucket = "base-terraform-remote-state"
    key = "base/terraform.tfstate"
    region = "us-west-2"
    dynamodb_table = "terraform-lock-table"

    s3_bucket_tags = {
      Owner = "UWMSIM-grp4"
      Name  = "UWMSIM-grp4_Terraform_remote_state_bucket"
      DeptCode = "460"
      Creator = "aftaba@uw.edu"
      Description = "Table to manage eats terrformlock"
      Group = "grop4"
      Application = "machinelearning pipeline"
      Environment = "base"
      }

    dynamodb_table_tags= {
      Owner = "UWMSIM-grp4"
      Name  = "UWMSIM-grp4_Terraform_remote_state_bucket"
      DeptCode = "460"
      Creator = "aftaba@uw.edu"
      Description = "Table to manage eats terrformlock"
      Group = "grop4"
      Application = "machinelearning pipeline"
      Environment = "base"
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