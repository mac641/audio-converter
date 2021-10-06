#!/bin/sh
set -e

if [ ! -f database.sqlite ]; then
  python3 create_db.py
fi

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- "$@"
fi

exec "$@"
