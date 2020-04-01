output "api_key" {
  value = "${aws_api_gateway_api_key.MyfirstAssignentkey.value}"
}

output "base_url" {
  value = "${aws_api_gateway_deployment.assignement1_stage_deployment.invoke_url}"
}