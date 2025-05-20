#!/bin/bash

python3 /odtp/odtp-app/app.py \
    --input /odtp/odtp-input/$INPUT_FILE \
    --output /odtp/odtp-output/$OUTPUT_FILE \
    --model $MODEL_NAME \
    --language $LANGUAGE \
    --endpoint $ENDPOINT \
    --api_key $API_KEY 
