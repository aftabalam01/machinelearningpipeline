
instance_type="t3.large"
instance_count_max="0"
instance_count_min="0"
instance_desired_count="0"
task_cpu=2048
task_memory=4096
# eats monitor db

db_username = "eats_service"
db_password = ""
db_name = "eats_service"
db_port = 5432
db_min_capacity=2
db_max_capacity=8
TAG_ENVIRONMENT="dev"

# Build info
branch="Dev"
build="latest"
metadata_auto_conf_url="https://tableausandbox.oktapreview.com/app/exkj0ydrjrFPhOjAP0h7/sso/saml/metadata"
entity_id="http://www.okta.com/exkj0ydrjrFPhOjAP0h7"
