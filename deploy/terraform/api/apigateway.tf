#https://learn.hashicorp.com/terraform/aws/lambda-api-gateway

resource "aws_api_gateway_account" "dga_predict" {
  cloudwatch_role_arn = "${aws_iam_role.apigateway_role.arn}"
}


resource "aws_iam_role" "apigateway_role" {
  name = "lambda-apigateway-role"
  description = "Lambda and Apigateway role"

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
  tags = "${merge(var.tags,map("Name" ,"Lambda and Apigateway role"))}"
}

resource "aws_iam_role_policy" "cloudwatch" {
  name = "default"
  role = "${aws_iam_role.apigateway_role.id}"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:DescribeLogGroups",
                "logs:DescribeLogStreams",
                "logs:PutLogEvents",
                "logs:GetLogEvents",
                "logs:FilterLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
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

# allow access log in cloudwatch
resource "aws_iam_role_policy_attachment" "api_cloudwatch_access" {
    role       = "${aws_iam_role.apigateway_role.name}"
    policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_api_key" "predict_api_key" {
  name = "predict_api_key"
  count = 2
}

resource "aws_api_gateway_api_key" "admin_api_key" {
  name = "admin_api_key"
  count = 2
}

resource "aws_api_gateway_rest_api" "dga_api_gateway" {
  name        = "dga_api_gateway"
  description = "Api gateway for dga predict, billing and apikeys"
}


resource "aws_api_gateway_request_validator" "request_validators" {
  name = "request_validators"
  rest_api_id = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
  validate_request_body = false
  validate_request_parameters = true
}


# root path integrated to mock#########

 resource "aws_api_gateway_method" "root_path" {
   rest_api_id   = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id   = aws_api_gateway_rest_api.dga_api_gateway.root_resource_id
   http_method   = "GET"
   authorization = "NONE"
   api_key_required = false
   request_validator_id = aws_api_gateway_request_validator.request_validators.id
   request_parameters = {"method.request.header.x-api-key" = true}
 }


 resource "aws_api_gateway_integration" "root_mock" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id = aws_api_gateway_method.root_path.resource_id
   http_method = aws_api_gateway_method.root_path.http_method

   integration_http_method = "POST"
   type                    = "MOCK"

 }


# /predict+ path integrated to lambda   #########
resource "aws_api_gateway_resource" "predict_path" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   parent_id   = aws_api_gateway_rest_api.dga_api_gateway.root_resource_id
   path_part   = "predict"
}

resource "aws_api_gateway_method" "predict_get" {
   rest_api_id   = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id   = aws_api_gateway_resource.predict_path.id
   http_method   = "GET"
   authorization = "NONE"
   api_key_required = true
   request_validator_id = aws_api_gateway_request_validator.request_validators.id
   request_parameters = {"method.request.header.x-api-key" = true ,"method.request.querystring.fqdn" = true}
 }

resource "aws_api_gateway_integration" "lambda_predict" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id = aws_api_gateway_method.predict_get.resource_id
   http_method = aws_api_gateway_method.predict_get.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda_predict.invoke_arn
   credentials = aws_iam_role.apigateway_role.arn
 }

# adding permission in lambda
resource "aws_lambda_permission" "allow_api_gateway_predict" {
    function_name = "${aws_lambda_function.lambda_assignment1.function_name}"
    statement_id = "AllowExecutionFromApiGateway"
    action = "lambda:InvokeFunction"
    principal = "apigateway.amazonaws.com"
    source_arn = "arn:aws:execute-api:${var.AWS_REGION}:${var.account_id}:${aws_api_gateway_rest_api.dga_api_gateway.id}/*/*/${aws_api_gateway_integration.lambda_predict.integration_http_method}${aws_api_gateway_resource.predict_path.path}"
}


# /billingingo+ path integrated to lambda   #########
resource "aws_api_gateway_resource" "billinginfo_path" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   parent_id   = aws_api_gateway_rest_api.dga_api_gateway.root_resource_id
   path_part   = "billinginfo"
}

resource "aws_api_gateway_method" "billinginfo_get" {
   rest_api_id   = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id   = aws_api_gateway_resource.billinginfo_path.id
   http_method   = "GET"
   authorization = "NONE"
   api_key_required = true
   request_validator_id = aws_api_gateway_request_validator.request_validators.id
   request_parameters = {"method.request.header.x-api-key" = true ,"method.request.querystring.api_id" = true,
   "method.request.querystring.startDate" = true,"method.request.querystring.endDate" = true}
 }

resource "aws_api_gateway_integration" "lambda_billinginfo" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id = aws_api_gateway_method.billinginfo_get.resource_id
   http_method = aws_api_gateway_method.billinginfo_get.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda_billinginfo.invoke_arn
   credentials = aws_iam_role.apigateway_role.arn
 }

# adding permission in lambda
resource "aws_lambda_permission" "allow_api_gateway_billinginfo" {
    function_name = "${aws_lambda_function.lambda_billinginfo.function_name}"
    statement_id = "AllowExecutionFromApiGateway"
    action = "lambda:InvokeFunction"
    principal = "apigateway.amazonaws.com"
    source_arn = "arn:aws:execute-api:${var.AWS_REGION}:${var.account_id}:${aws_api_gateway_rest_api.dga_api_gateway.id}/*/*/${aws_api_gateway_integration.lambda_billinginfo.integration_http_method}${aws_api_gateway_resource.billinginfo_path.path}"
}


# /getapis+ path integrated to lambda   #########
resource "aws_api_gateway_resource" "getapis_path" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   parent_id   = aws_api_gateway_rest_api.dga_api_gateway.root_resource_id
   path_part   = "getapis"
}

resource "aws_api_gateway_method" "getapis_get" {
   rest_api_id   = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id   = aws_api_gateway_resource.getapis_path.id
   http_method   = "GET"
   authorization = "NONE"
   api_key_required = true
   request_validator_id = aws_api_gateway_request_validator.request_validators.id
   request_parameters = {"method.request.header.x-api-key" = true }
 }

resource "aws_api_gateway_integration" "lambda_getapis" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id = aws_api_gateway_method.getapis_get.resource_id
   http_method = aws_api_gateway_method.getapis_get.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda_getapi_key.invoke_arn
   credentials = aws_iam_role.apigateway_role.arn
 }

# adding permission in lambda
resource "aws_lambda_permission" "allow_api_gateway_getapis" {
    function_name = "${aws_lambda_function.lambda_getapi_key.function_name}"
    statement_id = "AllowExecutionFromApiGateway"
    action = "lambda:InvokeFunction"
    principal = "apigateway.amazonaws.com"
    source_arn = "arn:aws:execute-api:${var.AWS_REGION}:${var.account_id}:${aws_api_gateway_rest_api.dga_api_gateway.id}/*/*/${aws_api_gateway_integration.lambda_getapis.integration_http_method}${aws_api_gateway_resource.getapis_path.path}"
}


# /createapiskey+ path integrated to lambda   #########
resource "aws_api_gateway_resource" "createapiskey_path" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   parent_id   = aws_api_gateway_rest_api.dga_api_gateway.root_resource_id
   path_part   = "createapiskey"
}

resource "aws_api_gateway_method" "createapiskey_post" {
   rest_api_id   = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id   = aws_api_gateway_resource.createapiskey_path.id
   http_method   = "POST"
   authorization = "NONE"
   api_key_required = true
   request_validator_id = aws_api_gateway_request_validator.request_validators.id
   request_parameters = {"method.request.header.x-api-key" = true ,"method.request.querystring.email" = true}
 }

resource "aws_api_gateway_integration" "lambda_createapiskey" {
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   resource_id = aws_api_gateway_method.createapiskey_post.resource_id
   http_method = aws_api_gateway_method.createapiskey_post.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.lambda_createapi_key.invoke_arn
   credentials = aws_iam_role.apigateway_role.arn
 }

# adding permission in lambda
resource "aws_lambda_permission" "allow_api_gateway_createapi" {
    function_name = "${aws_lambda_function.lambda_createapi_key.function_name}"
    statement_id = "AllowExecutionFromApiGateway"
    action = "lambda:InvokeFunction"
    principal = "apigateway.amazonaws.com"
    source_arn = "arn:aws:execute-api:${var.AWS_REGION}:${var.account_id}:${aws_api_gateway_rest_api.dga_api_gateway.id}/*/*/${aws_api_gateway_integration.lambda_createapiskey.integration_http_method}${aws_api_gateway_resource.createapiskey_path.path}"
}


// can not use aws_api_gateway_stage and aws_api_gateway_deployment together due to circular dependency
/*
resource "aws_api_gateway_stage" "stage" {
  stage_name    = "stage"
  rest_api_id   = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
  deployment_id = "${aws_api_gateway_deployment.api_deployment_stage.id}"
}

resource "aws_api_gateway_stage" "prod" {
  stage_name    = "prod"
  rest_api_id   = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
  deployment_id = "${aws_api_gateway_deployment.api_deployment_prod.id}"
}
*/
resource "aws_api_gateway_deployment" "api_deployment_stage_predict" {
   depends_on = [aws_api_gateway_integration.lambda_predict, aws_api_gateway_integration.root_mock, ]
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   stage_name  = "stage_predict"
 }

resource "aws_api_gateway_deployment" "api_deployment_prod_predict" {
   depends_on = [aws_api_gateway_integration.lambda_predict, aws_api_gateway_integration.root_mock, ]
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   stage_name  = "prod_predict"
 }

resource "aws_api_gateway_deployment" "api_deployment_stage_admin" {
   depends_on = [aws_api_gateway_integration.lambda_predict, aws_api_gateway_integration.root_mock, ]
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   stage_name  = "stage_admin"
 }

resource "aws_api_gateway_deployment" "api_deployment_prod_admin" {
   depends_on = [aws_api_gateway_integration.lambda_predict, aws_api_gateway_integration.root_mock, ]
   rest_api_id = aws_api_gateway_rest_api.dga_api_gateway.id
   stage_name  = "prod_admin"
 }


### create stage usage plan and add it to key###

resource "aws_api_gateway_usage_plan" "PredictUsagePlan" {
  name         = "predict-usage-plan"
  description  = "predict usage description"
  product_code = "predict_product_code"

  api_stages {
    api_id = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
    stage  = "${aws_api_gateway_deployment.api_deployment_stage_predict.stage_name}"
  }
  api_stages {
    api_id = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
    stage  = "${aws_api_gateway_deployment.api_deployment_prod_predict.stage_name}"
  }


  quota_settings {
    limit  = 1000
    offset = 0
    period = "DAY"
  }

  throttle_settings {
    burst_limit = 10
    rate_limit  = 100
  }
}
resource "aws_api_gateway_usage_plan_key" "stage_predict_api_plan" {
  key_id        = "${aws_api_gateway_api_key.predict_api_key[0].id}"
  key_type      = "API_KEY"
  usage_plan_id = "${aws_api_gateway_usage_plan.PredictUsagePlan.id}"
}

resource "aws_api_gateway_usage_plan_key" "stage_billing_api_plan" {
  key_id        = "${aws_api_gateway_api_key.billing_api_key[0].id}"
  key_type      = "API_KEY"
  usage_plan_id = "${aws_api_gateway_usage_plan.StageUsagePlan.id}"
}

### create usage plan and add it to key###

resource "aws_api_gateway_usage_plan" "ProdUsagePlan" {
  name         = "Prod-usage-plan"
  description  = "production usages description"
  product_code = "My product"

  api_stages {
    api_id = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
    stage  = "${aws_api_gateway_deployment.api_deployment_prod.stage_name}"
  }


  quota_settings {
    limit  = 10000
    offset = 0
    period = "DAY"
  }

  throttle_settings {
    burst_limit = 10
    rate_limit  = 100
  }
}
resource "aws_api_gateway_usage_plan_key" "prod_predict_api_plan" {
  key_id = "${aws_api_gateway_api_key.predict_api_key[1].id}"
  key_type = "API_KEY"
  usage_plan_id = "${aws_api_gateway_usage_plan.ProdUsagePlan.id}"
}

resource "aws_api_gateway_usage_plan_key" "prod_billing_api_plan" {
  key_id = "${aws_api_gateway_api_key.billing_api_key[1].id}"
  key_type = "API_KEY"
  usage_plan_id = "${aws_api_gateway_usage_plan.ProdUsagePlan.id}"
}

# enable metrics for predict calls in  stageooooo

resource "aws_api_gateway_method_settings" "predict_stage" {
  rest_api_id = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
  stage_name  = "${aws_api_gateway_deployment.api_deployment_stage.stage_name}"
  method_path = "${aws_api_gateway_resource.predict_path.path_part}/${aws_api_gateway_method.predict_get.http_method}"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}

# enable metrics for predict calls in  prod

resource "aws_api_gateway_method_settings" "predict_prod" {
  rest_api_id = "${aws_api_gateway_rest_api.dga_api_gateway.id}"
  stage_name  = "${aws_api_gateway_deployment.api_deployment_prod.stage_name}"
  method_path = "${aws_api_gateway_resource.predict_path.path_part}/${aws_api_gateway_method.predict_get.http_method}"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}