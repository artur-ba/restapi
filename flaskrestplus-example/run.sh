#!/bin/sh

cpu_cores=$(nproc --all)
workers_count=$((((cpu_cores) *2 ) + 1))

gunicorn \
    --log-config ./logging.conf \
    --bind 0.0.0.0:3001 \
    --workers "${workers_count}" \
    --worker-class eventlet \
    --timeout 500 \
    --preload \
    service.app:application
