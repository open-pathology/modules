# syntax=docker/dockerfile:1
FROM python:3.12 AS base

RUN --mount=type=secret,id=pip,dst=/etc/pip.conf \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir scikit-image

WORKDIR /src

# stage used for module runtime
FROM base AS main
COPY main.py module.json /src/

CMD ["python3", "main.py"]

# stage used for module linting and tests
FROM base AS test
RUN --mount=type=secret,id=pip,dst=/etc/pip.conf \
    python3 -m pip install --no-cache-dir pytest ruff

COPY . /src/
