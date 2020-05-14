#https://learn.hashicorp.com/terraform/aws/lambda-api-gateway

resource "aws_iam_role" "apigateway_role" {
  name = "Assignment1-apigateway-role"
  description = "Assignment1-apigateway -role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "apigateway.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
}
EOF
  tags = "${merge(var.tags,map("Name" ,"Assignment1-apigateway-role"))}"
}

# attach policy to all apigateway access

# Attach policies to apigateway_role

resource "aws_iam_role_policy_attachment" "apigateway_full_access" {
    role       = "${aws_iam_role.apigateway_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess"
}

resource "aws_iam_role_policy_attachment" "api_lambda_full_access" {
    role       = "${aws_iam_role.apigateway_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}
resource "aws_api_gateway_api_key" "MyfirstAssignentkey" {
  name = "MyfirstAssignentkey"
}

resource "aws_api_gateway_rest_api" "assignement1" {
  name        = "assignment1_api"
  description = "Terraform Serverless Application Example"
}

resource "aws_api_gateway_resource" "proxy" {
   rest_api_id = aws_api_gateway_rest_api.assignement1.id
   parent_id   = aws_api_gateway_rest_api.assignement1.root_resource_id
   path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
   rest_api_id   = aws_api_gateway_rest_api.assignement1.id
   resource_id   = aws_api_gateway_resource.proxy.id
   http_method   = "ANY"
   authorization = "NONE"
   request_parameters = {"method.request.header.X-CUSTOMER-API-KEY" = true ,"method.request.querystring.fqdn" = true}
 }

resource "aws_api_gateway_integration" "lambda" {
   rest_api_id = aws_api_gateway_rest_api.assignement1.id
   resource_id = aws_api_gateway_method.proxy.resource_id
   http_method = aws_api_gateway_method.proxy.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda_assignment1.invoke_arn
   credentials = aws_iam_role.apigateway_role.arn
 }


 resource "aws_api_gateway_method" "proxy_root" {
   rest_api_id   = aws_api_gateway_rest_api.assignement1.id
   resource_id   = aws_api_gateway_rest_api.assignement1.root_resource_id
   http_method   = "ANY"
   authorization = "NONE"
   request_parameters = {"method.request.header.X-CUSTOMER-API-KEY" = true ,"method.request.querystring.fqdn" = true}
 }

 resource "aws_api_gateway_integration" "lambda_root" {
   rest_api_id = aws_api_gateway_rest_api.assignement1.id
   resource_id = aws_api_gateway_method.proxy_root.resource_id
   http_method = aws_api_gateway_method.proxy_root.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda_assignment1.invoke_arn
   credentials = aws_iam_role.apigateway_role.arn
 }


resource "aws_api_gateway_deployment" "assignement1_stage_deployment" {
   depends_on = [aws_api_gateway_integration.lambda,aws_api_gateway_integration.lambda_root, ]

   rest_api_id = aws_api_gateway_rest_api.assignement1.id
   stage_name  = "stage"
 }


# adding permission in lambda
resource "aws_lambda_permission" "allow_api_gateway_root" {
    function_name = "${aws_lambda_function.lambda_assignment1.function_name}"
    statement_id = "AllowExecutionFromApiGateway_root"
    action = "lambda:InvokeFunction"
    principal = "apigateway.amazonaws.com"
    source_arn = "arn:aws:execute-api:${var.AWS_REGION}:${var.account_id}:${aws_api_gateway_rest_api.assignement1.id}/*/${aws_api_gateway_integration.lambda_root.integration_http_method}${aws_api_gateway_resource.proxy.path}"
}

# adding permission in lambda
resource "aws_lambda_permission" "allow_api_gateway" {
    function_name = "${aws_lambda_function.lambda_assignment1.function_name}"
    statement_id = "AllowExecutionFromApiGateway"
    action = "lambda:InvokeFunction"
    principal = "apigateway.amazonaws.com"
    source_arn = "arn:aws:execute-api:${var.AWS_REGION}:${var.account_id}:${aws_api_gateway_rest_api.assignement1.id}/*/${aws_api_gateway_integration.lambda.integration_http_method}${aws_api_gateway_resource.proxy.path}"
}