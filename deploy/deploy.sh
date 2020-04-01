#!/usr/bin/env bash
# clear previous cache file
# usages ./deploy.sh -e dev -c plan
# ./deploy.sh -e dev -c apply -a true

while getopts e:c:a option
do
case "${option}"
in
e) ENV=${OPTARG};;
d) TFCMD=${OPTARG};;
a) APPROVE=${OPTARG};;
esac
done
curr_dir=${pwd}
echo "current dir is $curr_dir"
if [ $TFCMD -eq "init" ]
then find . -type d -name ".terragrunt-cache" -prune -exec rm -rf {} \;
fi
if [[ ($TFCMD -eq "apply" || $TFCMD -eq "destroy" ) && ( $APPROVE -eq 'true' ) ]]
then
 docker_cmd=`echo "docker run -it --rm -v $curr_dir:/apps/ -v ~/.aws:/root/.aws -e AWS_DEFAULT_PROFILE=aftabuw -w /apps/$ENV aftabalam01/terragrunt:0.19.25 $TFCMD -auto-approve"`
else
 docker_cmd=`echo "docker run -it --rm -v $curr_dir:/apps/ -v ~/.aws:/root/.aws -e AWS_DEFAULT_PROFILE=aftabuw -w /apps/$ENV aftabalam01/terragrunt:0.19.25 $TFCMD"`
fi

echo "Running docker command " $docker_cmd
eval " $docker_cmd"