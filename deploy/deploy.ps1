# powershell script to run terragrunt/terraform container
param (
    [Parameter(Mandatory=$true)][string]$env = $( Read-Host "Please enter env" ),
    [Parameter(Mandatory=$true)][string]$tfcmd = $( Read-Host "Please enter terraform command" ),
    [Parameter(Mandatory=$false)][string]$tfapprove = $( Read-Host "If command is apply/destroy, please tell if auto approve true/false" )
 )
Write-Output "Current Directory is '${PWD}'"

if( $tfapprove  -and  $tfcmd -eq 'apply' ){
$docker_cmd = "docker run -it --rm -v ${PWD}:/apps/ -v $env:USERPROFILE\.aws:/root/.aws -e AWS_DEFAULT_PROFILE=aftabuw -w /apps/deploy/$env aftabalam01/terragrunt:0.19.25 $tfcmd -auto-approve"
} Else{
$docker_cmd = "docker run -it --rm -v ${PWD}:/apps/ -v $env:USERPROFILE\.aws:/root/.aws -e AWS_DEFAULT_PROFILE=aftabuw -w /apps/deploy/$env aftabalam01/terragrunt:0.19.25 $tfcmd"
}
Write-Output " Starting '$docker_cmd'"
Invoke-Expression $docker_cmd
