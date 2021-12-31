#!/bin/sh
set -e

if [ ! -f media/database.sqlite ]; then
  python3 create_db.py
fi

if [ "${1#-}" != "${1}" ] || [ -z "$(command -v "${1}")" ]; then
  set -- "$@"
fi

exec "$@"
