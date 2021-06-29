#!/usr/bin/env bash

aws configure set default.s3.signature_version s3v4
aws configure set aws_region $AWS_REGION
aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
