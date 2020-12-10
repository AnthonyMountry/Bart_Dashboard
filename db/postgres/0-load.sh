#!/bin/bash

pg_restore -d $POSTGRES_DB -U $POSTGRES_USER -Fc -j $(nproc) /docker-entrypoint-initdb.d/database.dump
