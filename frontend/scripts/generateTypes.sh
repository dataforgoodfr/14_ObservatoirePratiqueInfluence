#!/bin/bash

set -a
source "$(dirname "$0")/../.env"
set +a

mkdir -p generated-types

# Fetch swagger.json depuis nocodb
curl -H "xc-token: $NOCODB_API_TOKEN" \
  "$NOCODB_BASE_URL/api/v3/meta/bases/$NOCODB_DATA_BASE_ID/swagger.json" \
  -o generated-types/swagger.json

# Ne conserver que les clés GET dans paths
node -e "
const fs = require('fs');
const swagger = JSON.parse(fs.readFileSync('generated-types/swagger.json', 'utf8'));
for (const path of Object.keys(swagger.paths || {})) {
  const methods = swagger.paths[path];
  for (const method of Object.keys(methods)) {
    if (method !== 'get') delete methods[method];
  }
  if (Object.keys(methods).length === 0) delete swagger.paths[path];
}
fs.writeFileSync('generated-types/swagger-get-only.json', JSON.stringify(swagger, null, 2));
"

# Générer les types TypeScript
npx swagger-typescript-api generate --patch --clean-output -p ./generated-types/swagger-get-only.json -o generated-types

# Supprimer les .json intermédiaires :
rm -rf ./generated-types/swagger.json
rm -rf ./generated-types/swagger-get-only.json
