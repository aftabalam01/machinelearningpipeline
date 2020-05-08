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

resource "aws_iam_role_policy_attachment" "lambda_apigateway_invoke_access" {
    role       = "${aws_iam_role.lambda_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_apigateway_admin_access" {
    role       = "${aws_iam_role.lambda_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator"
}

resource "aws_iam_role_policy_attachment" "lambda_full_access" {
    role       = "${aws_iam_role.lambda_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}


data "aws_s3_bucket" "uw-imt575" {
  bucket = "imt573-g3-databucket"
}

# create lambda layer
resource "aws_s3_bucket_object" "layer" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "lambda/lambda_layer_req_boto_tld.zip"
  source = "${path.module}/lambda_layer/lambda_layer_req_boto_tld.zip"
}

resource "aws_lambda_layer_version" "requests_sign_boto3" {
  layer_name = "lambda_layer_name"
  depends_on = [aws_s3_bucket_object.layer]
  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "lambda/lambda_layer_req_boto_tld.zip"
  source_code_hash = "${filebase64sha256("api/lambda_layer/lambda_layer_req_boto_tld.zip")}"
  compatible_runtimes = ["python3.7"]
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
  runtime = "python3.7"
  depends_on = [aws_s3_bucket_object.Assignment1]
  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "Assignment1/basic_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/basic_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "Assingment1 lambda function"))}"
}


resource "aws_s3_bucket_object" "predict" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "lambda/predict_lambda_function.zip"
  source = "${path.module}/predict_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_predict" {
  function_name = "predict_lambda_function"
  handler = "predict_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.7"
  depends_on = [aws_s3_bucket_object.predict]
  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "lambda/predict_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/predict_lambda_function.zip")}"
  timeout = 30
  memory_size = 128
  layers = ["${aws_lambda_layer_version.requests_sign_boto3.arn}"]

  tags = "${merge(var.tags,map("Name" , "predict_lambda_function"))}"
}

resource "aws_s3_bucket_object" "billinginfo" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "lambda/billinginfo_lambda_function.zip"
  source = "${path.module}/billinginfo_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_billinginfo" {
  function_name = "billinginfo_lambda_function"
  handler = "billinginfo_lambda_function.handler_using_db"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.7"
  depends_on = [aws_s3_bucket_object.billinginfo]
  layers = ["${aws_lambda_layer_version.requests_sign_boto3.arn}"]
  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "lambda/billinginfo_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/billinginfo_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "billinginfo_lambda_function"))}"
}

resource "aws_s3_bucket_object" "getapikey" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "lambda/getapis_lambda_function.zip"
  source = "${path.module}/getapis_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_getapi_key" {
  function_name = "getapis_lambda_function"
  handler = "getapis_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.7"
  depends_on = [aws_s3_bucket_object.getapikey]
  layers = ["${aws_lambda_layer_version.requests_sign_boto3.arn}"]
  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "lambda/getapis_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/getapis_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "getapis_lambda_function"))}"
}

resource "aws_s3_bucket_object" "createapikey" {
  bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  key    = "lambda/createapikey_lambda_function.zip"
  source = "${path.module}/createapikey_lambda_function.zip"
}


# create lambda function
resource "aws_lambda_function" "lambda_createapi_key" {
  function_name = "createapikey_lambda_function"
  handler = "createapikey_lambda_function.handler"
  role = "${aws_iam_role.lambda_role.arn}"
  runtime = "python3.7"
  depends_on = [aws_s3_bucket_object.createapikey]
  layers = ["${aws_lambda_layer_version.requests_sign_boto3.arn}"]
  s3_bucket = "${data.aws_s3_bucket.uw-imt575.id}"
  s3_key    = "lambda/createapikey_lambda_function.zip"
  source_code_hash = "${filebase64sha256("api/createapikey_lambda_function.zip")}"
  timeout = 30
  memory_size = 128

  tags = "${merge(var.tags,map("Name" , "lambda_createapi_key"))}"
}