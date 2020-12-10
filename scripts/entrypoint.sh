#!/bin/sh

if [ "$1" = "init" ]; then
    flask db init
    flask db migrate
    flask db upgrade
    shift
fi

exec "$@"
