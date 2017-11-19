#!/bin/bash -e
set -ex # Abort on error

AWS_BUCKET=hrchatbot
STACK=hr-chatbot

git pull origin master
rm -f chatbot.json

zip -j Bot.zip LambdaFunctions/Bot/* 

aws s3 cp Bot.zip s3://hrchatbot/Bot.zip

#rm -f Bot.zip

# Package the Lambda functions and create a hashtag as filename to force an update of the stack
aws cloudformation package --template CloudFormation/chatbot.yaml --s3-bucket hrchatbot --output json > chatbot.json

# Update the stack
aws cloudformation deploy --region us-east-1 --template chatbot.json --stack-name $STACK --capabilities  CAPABILITY_IAM