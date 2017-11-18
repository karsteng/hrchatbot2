#!/bin/bash -e
set -ex # Abort on error

./secrets.sh

AWS_BUCKET=hrchatbot
STACK=hr-chatbot

git pull origin master
rm -f chatbot.json

# Package the Lambda functions and create a hashtag as filename to force an update of the stack
aws cloudformation package --template CloudFormation/chatbot.yaml --s3-bucket hrchatbot --output json > chatbot.json

# Update the stack
aws cloudformation deploy --region us-east-1 --template chatbot.json --stack-name $STACK --capabilities  CAPABILITY_IAM

# Update the slot types
create-slot-type-version --name JobLevel --cli-input-json $(< LambdaFunctions\bot\job_level_types.json)
create-slot-type-version --name JobLocation --cli-input-json $(< LambdaFunctions\bot\job_location_types.json)
create-slot-type-version --name JobPosition --cli-input-json $(< LambdaFunctions\bot\job_position_types.json)
