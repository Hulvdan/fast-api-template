#!/usr/bin/env sh

set -o errexit
set -o nounset

readonly cmd="$*"

postgres_ready() {
  # Check that postgres is up and running on port `5432`:
  dockerize -wait "tcp://${BACKEND_DATABASE_HOST}:${BACKEND_DATABASE_PORT}" -timeout 10s
}

# We need this line to make sure that this container is started
# after the one with postgres:
until postgres_ready; do
  echo >&2 'Postgres is unavailable - sleeping'
done

# It is also possible to wait for other services as well: redis, elastic, mongo
echo >&2 'Postgres is up - continuing...'

# Applying migrations
echo >&2 'Applying migrations...'
sh scripts/migrate.sh head

# Evaluating passed command (do not touch):
# shellcheck disable=SC2086
exec $cmd
