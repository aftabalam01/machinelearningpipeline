#! /bin/sh


# docker command to run terraform
build=$1
branch=$2
metadata_auto_conf_url=$3
entity_id=$4
task_cpu=$5
task_memory=$6
env=$7

echo "Current dir is `${PWD}`"
echo " Deploy param are: $1 $2 $3 $4 $5 $6 $7"


# initialize terraform
docker run --rm -v ${PWD}:/apps/ -w /apps/$env  \
-e AWS_DEFAULT_REGION=us-west-2 \
-e AWS_ACCESS_KEY_ID=$bamboo_aws_dev_access_key_id \
-e AWS_SECRET_ACCESS_KEY=$bamboo_aws_dev_secret_key \
aftabalam01/terragrunt:0.19.25  \
init 

# Apply with auto approval
docker run --rm -v ${PWD}:/apps/ -w /apps/$env  \
-e AWS_DEFAULT_REGION=us-west-2 \
-e AWS_ACCESS_KEY_ID=$bamboo_aws_dev_access_key_id \
-e AWS_SECRET_ACCESS_KEY=$bamboo_aws_dev_secret_key \
aftabalam01/terragrunt:0.19.25  \
apply -auto-approve \
-var="build=$1" \
-var="branch=$2" \
-var="metadata_auto_conf_url=$3" \
-var="entity_id=$4" \
-var="task_cpu=$5" \
-var="task_memory=$6" 

