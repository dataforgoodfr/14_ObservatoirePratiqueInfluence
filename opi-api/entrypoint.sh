#!/bin/bash

set -eu

# Run migrations
echo "run db migration"

./migrate -path migrations -database "$POSTGRES_DSN" -verbose up

# Run the application
source /opi-api/.venv/bin/activate
exec opi-api --host ${HOST} --port ${PORT} --reload ${RELOAD}
