#!/bin/sh

echo "Waiting for postgres:"

flask db init
flask db migrate
flask db upgrade

exec "$@"
