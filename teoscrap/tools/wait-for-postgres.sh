#!/bin/bash

echo "Waiting for postgres"

while ! nc -z $1; do
    sleep 1
done

echo "Postgres is OK, going on..."

shift
exec $@
