# define labmda role that is needed for execution
resource "aws_iam_role" "lambda_role" {
  name = "Assignment1-lambda-role"
  description = "Assignment1-lambda-role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
}
EOF
  tags = "${merge(var.tags,map("Name" ,"Assignment1-lambda-role"))}"
}

# attach policy to all apigateway access

# Attach policies to lambda role

resource "aws_iam_role_policy_attachment" "lambda_apigateway_full_access" {
    role       = "${aws_iam_role.lambda_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_full_access" {
    role       = "${aws_iam_role.lambda_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}

resource "aws_s3_bucket" "uw-imt573" {
  bucket = "my-test-bucket-imt575"
  acl = "private"

  tags =  "${merge(var.tags,map("Name" , "Assignment source bucket"))}"
}

resource "aws_s3_bucket_object" "object" {
  bucket = "${aws_s3_bucket.uw-imt573.bucket}"
  key    = "Assignment1/basic_lambda_function.zip"
  source = "${path.module}/basic_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_assignment1" {
  function_name = "Assingment1_lambda_function"
  handler = "basic_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.6"

  s3_bucket = "my-test-bucket-imt575"
  s3_key    = "Assignment1/basic_lambda_function.zip"
  source_code_hash = "${filebase64sha256("Assignment1/basic_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "Assingment1 lambda function "))}"
}