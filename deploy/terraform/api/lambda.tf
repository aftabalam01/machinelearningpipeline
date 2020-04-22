# define labmda role that is needed for execution
resource "aws_iam_role" "lambda_role" {
  name = "execution-lambda-role"
  description = "execution-lambda-role"

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
  tags = "${merge(var.tags,map("Name" ,"execution-lambda-role"))}"
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

data "aws_s3_bucket" "uw-imt575" {
  bucket = "imt573-g3-databucket"
}

resource "aws_s3_bucket_object" "Assignment1" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "Assignment1/basic_lambda_function.zip"
  source = "${path.module}/basic_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_assignment1" {
    function_name = "Assingment1_lambda_function"
  handler = "basic_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.6"

  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "Assignment1/basic_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/basic_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "Assingment1 lambda function"))}"
}


resource "aws_s3_bucket_object" "getapikeys" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "lambda/getapis_lambda_function.zip"
  source = "${path.module}/getapis_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_predict" {
  function_name = "predict_lambda_function"
  handler = "predict_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.6"

  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "lambda/predict_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/predict_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "predict_lambda_function"))}"
}

resource "aws_s3_bucket_object" "billinginfo" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "labmda/billinginfo_lambda_function.zip"
  source = "${path.module}/billinginfo_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_billinginfo" {
  function_name = "billinginfo_lambda_function"
  handler = "billinginfo_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.6"

  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "labmda/billinginfo_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/billinginfo_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "billinginfo_lambda_function"))}"
}

resource "aws_s3_bucket_object" "getapikey" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "labmda/getapis_lambda_function.zip"
  source = "${path.module}/getapis_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_getapi_key" {
  function_name = "getapis_lambda_function"
  handler = "getapis_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.6"

  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "labmda/getapis_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/getapis_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "getapis_lambda_function"))}"
}

resource "aws_s3_bucket_object" "createapikey" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "labmda/createapikey_lambda_function.zip"
  source = "${path.module}/createapikey_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_createapi_key" {
  function_name = "createapikey_lambda_function"
  handler = "createapikey_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.6"

  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "labmda/createapikey_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/createapikey_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "lambda_createapi_key"))}"
}