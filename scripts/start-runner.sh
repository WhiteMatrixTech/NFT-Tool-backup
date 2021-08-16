#!/usr/bin/env bash

aws s3 cp s3://${AWS_S3_BUCKET}/data.zip .
rm -rf /data
unzip -o data.zip -d /data
pipenv run normalizedata
sleep infinity

