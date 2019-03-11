FROM python:3.7.2-alpine3.8 as base

WORKDIR /app

RUN apk --update \
    add --no-cache --virtual build_dependencies \
        alpine-sdk=1.0-r0 \
        libc-dev=0.7.1-r0 \
        libffi-dev=3.2.1-r4 \
        libressl-dev=2.7.5-r0 \
        postgresql-dev=10.5-r0 \
        python3-dev=3.6.6-r0 && \
    pip install --upgrade pip==19.0.1

COPY requirements.txt ./
RUN pip install -r ./requirements.txt && \
    rm -rf ./requirements.txt

FROM base as verify

WORKDIR /app
ENV PYTHONPATH=/app

COPY . ./
RUN pip install -r ./test-requirements.txt

RUN yapf --recursive --diff ./service
RUN mypy --config-file ./mypy.ini ./service
RUN flake8 --jobs 1 --config ./.flake8 ./service

FROM base as cleanup

RUN apk del build_dependencies && \
    rm -rf /root/.cache

FROM cleanup as production

WORKDIR /app
ENV PYTHONPATH=/app

RUN apd add --no-cache \
    tini=0.18.0-r0 \
    py3-psycopg2=2.7.5-r0

RUN addgroup -S app && adduser -S app -G app

COPY logging.conf run.sh ./
COPY service ./service

USER app:app

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["./run.sh"]