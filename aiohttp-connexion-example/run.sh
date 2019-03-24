#!/bin/sh

cpu_cores=$(nproc --all)
workers_count=$((((cpu_cores) *2 ) + 1))

/usr/local/bin/gunicorn \
  --log-config ./logging.conf \
  --bind 0.0.0.0:3003 \
  --workers "${workers_count}" \
  --worker-class aiohttp.worker.GunicornUVLoopWebWorker \
  service.app:application
