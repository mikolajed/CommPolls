#!/bin/sh

# wait_for_db.sh

set -e

host="$1"
shift
cmd="$@"

export PGPASSWORD=$DB_PASSWORD

until psql -h "$host" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  echo "Postgres is unavailable — sleeping"
  sleep 1
done

exec $cmd
