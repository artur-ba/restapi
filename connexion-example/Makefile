run_gunicorn = gunicorn --log-config logging.conf --reload --workers 5 --worker-class eventlet --timeout 500  --bind 0.0.0.0:3002 "service.app:application"


docker-lint:
	docker run --rm -i hadolint/hadolint < ./Dockerfile

docker-build: docker-lint
	docker build \
		-t flaskrestful/service \
		.

docker-run: docker-build
	docker run --rm -it \
		-p 3002:3002 \
		--net=host \
		-v $(shell pwd):/app \
		flaskrestful/service \
		sh -c '${run_gunicorn}'
