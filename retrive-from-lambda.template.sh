#!/bin/bash

export AWS_REGION=''
export AWS_KEY_ID=''
export AWS_KEY_SECRET=''
export URL='' #aws lambda url

curl --aws-sigv4 "aws:amz:${AWS_REGION}:lambda"\
    --user "${AWS_KEY_ID}:${AWS_KEY_SECRET}"\
    $URL
