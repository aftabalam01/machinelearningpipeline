resource "aws_dynamodb_table" "apikeys" {
  name           = "apikeys"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "apikeyId"
  range_key      = "email"

  attribute {
    name = "apikeyId"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }


  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}

resource "aws_dynamodb_table" "apicalllog" {
  name           = "apicalllog"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "requestTime"
  range_key      = "apikeyId"

  attribute {
    name = "requestTime"
    type = "S"
  }

  attribute {
    name = "apikeyId"
    type = "S"
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}