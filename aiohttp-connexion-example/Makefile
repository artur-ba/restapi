run_gunicorn = gunicorn --workers 5 --worker-class aiohttp.worker.GunicornUVLoopWebWorker --log-config logging.conf --reload --bind 0.0.0.0:3003 "service.app:application"


docker-lint:
	docker run --rm -i hadolint/hadolint < ./Dockerfile

docker-build: docker-lint
	docker build \
		-t aiohttp-connexion/service \
		.

docker-run: docker-build
	docker run --rm -it \
		-p 3003:3003 \
		--net=host \
		-v $(shell pwd):/app \
		aiohttp-connexion/service \
		sh -c '${run_gunicorn}'
