output "prod_predict_api_key" {
  value = "${aws_api_gateway_api_key.predict_api_key[1].value}"
}

output "prod_billing_api_key" {
  value = "${aws_api_gateway_api_key.billing_api_key[1].value}"
}

output "prod_url" {
  value = "${aws_api_gateway_deployment.api_deployment_prod.invoke_url}"
}

output "stage_predict_api_key" {
  value = "${aws_api_gateway_api_key.predict_api_key[0].value}"
}

output "stage_billing_api_key" {
  value = "${aws_api_gateway_api_key.billing_api_key[0].value}"
}
output "stage_url" {
  value = "${aws_api_gateway_deployment.api_deployment_stage.invoke_url}"
}