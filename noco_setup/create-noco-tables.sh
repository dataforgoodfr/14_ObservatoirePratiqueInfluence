#!/bin/bash

## Define this in env
# NOCO_BASE_ID=<the base where to create the tables>
# NOCO_URL=<the Noco isntance base url e.g. http://localhost:8080>
# NOCO_API_TOKEN=<Noco personnal api token>
set -e


[[ -z "${NOCO_BASE_ID}" ]] && echo "NOCO_BASE_ID needs to be defined" && exit
[[ -z "${NOCO_URL}" ]] && echo "NOCO_URL needs to be defined" && exit
[[ -z "${NOCO_API_TOKEN}" ]] && echo "NOCO_API_TOKEN needs to be defined" && exit


mkdir -p .tmp

curl -X POST \
"$NOCO_URL/api/v3/meta/bases/$NOCO_BASE_ID/tables" \
-o .tmp/create_post_response.json \
-H "Content-Type: application/json" \
-H "xc-token: $NOCO_API_TOKEN" \
-d @create_post_table_payload.json

POST_TABLE_ID=$(cat .tmp/create_post_response.json | jq -r '.id')
echo POST_TABLE_ID : $POST_TABLE_ID
sed "s/POST_TABLE_ID/$POST_TABLE_ID/" create_account_table_payload.json > .tmp/create_account_table_payload.json


curl -X POST \
"$NOCO_URL/api/v3/meta/bases/$NOCO_BASE_ID/tables" \
-o .tmp/create_account_response.json \
-H "Content-Type: application/json" \
-H "xc-token: $NOCO_API_TOKEN" \
-d @.tmp/create_account_table_payload.json
